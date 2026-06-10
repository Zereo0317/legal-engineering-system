"""Westlaw MCP Server — unified legal research across multiple sources.

Combines WestLaw Classic (Playwright scraper), CourtListener, Congress.gov,
Federal Register, eCFR, EUR-Lex, Taiwan Judicial Yuan, EU Compliance,
OECD Tax Treaties, SEC EDGAR, and Singapore eLitigation into a single
MCP server with 21 tools.

Westlaw Classic requires institutional subscription — if it fails, tools
automatically fall back to CourtListener (free, US case law).
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

from .errors import make_empty_result, make_error
from contextlib import contextmanager

from .clients import congress as congress_client
from .clients import courtlistener, ecfr, eurlex, federal_register, westlaw_classic
from .clients import taiwan_judicial, eu_compliance, oecd_treaties, sec_edgar, singapore_elit
from .clients.base import get_all_breaker_health


class _NoopTracker:
    def set_result(self, _: Any) -> None:
        pass


@contextmanager
def tool_tracker(name: str, params: dict | None = None):
    t = _NoopTracker()
    try:
        yield t
    except Exception:
        raise
from .models import (
    CaseGetInput,
    CaseSearchInput,
    CFRSectionInput,
    EUComplianceArticleInput,
    EUComplianceCompareInput,
    EUComplianceSearchInput,
    OECDMLIStatusInput,
    OECDModelConventionInput,
    OECDTreatyInput,
    RegulationSearchInput,
    ResponseFormat,
    SECFilingGetInput,
    SECFilingSearchInput,
    SECFullTextSearchInput,
    SingaporeCaseSearchInput,
    SingaporeJudgmentGetInput,
    TaiwanInterpretationSearchInput,
    TaiwanJudgmentSearchInput,
    TaiwanStatuteInput,
    UnifiedSearchInput,
)

logger = logging.getLogger(__name__)

mcp = FastMCP(
    "westlaw_mcp",
    instructions=(
        "Unified legal research — 21 tools across 11 legal databases. "
        "FREE (no API key): westlaw_search_cases (CourtListener, 3,352 US courts), "
        "westlaw_search_regulations (Federal Register), westlaw_get_cfr_section (eCFR full text), "
        "westlaw_search_eu_law (EUR-Lex), westlaw_search_taiwan_judgments (Taiwan Judicial Yuan), "
        "westlaw_get_taiwan_statute (Taiwan statutes), westlaw_search_taiwan_interpretations, "
        "westlaw_eu_compliance_search (GDPR/AI Act/DSA), westlaw_eu_compliance_article, "
        "westlaw_eu_compliance_compare, westlaw_search_sec_filings (SEC EDGAR), "
        "westlaw_get_sec_filing, westlaw_sec_full_text_search, "
        "westlaw_search_singapore_cases (eLitigation), westlaw_get_singapore_judgment. "
        "FREE API KEY REQUIRED: westlaw_search_legislation (Congress.gov), "
        "westlaw_oecd_get_treaty, westlaw_oecd_model_convention, westlaw_oecd_commentary, "
        "westlaw_oecd_mli_status. "
        "INSTITUTIONAL SUBSCRIPTION: westlaw_classic_search, westlaw_classic_get_document "
        "(auto-falls back to CourtListener if Westlaw unavailable). "
        "MULTI-SOURCE: westlaw_unified_search queries cases + legislation + regulations + EU law "
        "in parallel. Start here for broad legal research."
    ),
)


# ── Helpers ────────────────────────────────────────────────────────────


def _format(data: dict, fmt: ResponseFormat) -> str:
    """Format results as Markdown or JSON."""
    if fmt == ResponseFormat.JSON:
        return json.dumps(data, ensure_ascii=False, indent=2)
    return _to_markdown(data)


def _to_markdown(data: dict) -> str:
    """Convert result dict to readable Markdown."""
    lines: list[str] = []

    # Normalise westlaw_classic old-style errors: {"error": "message string"}
    if "error" in data and "message" not in data:
        data = {
            "error": "upstream_error",
            "message": data["error"],
            **{k: v for k, v in data.items() if k != "error"},
        }

    # Unified error handling
    if "error" in data:
        lines.append(f"**Error** ({data['error']}): {data.get('message', '')}")
        if data.get("suggestions"):
            lines.append("\n**Suggestions:**")
            for s in data["suggestions"]:
                lines.append(f"- {s}")
        if data.get("retryable"):
            retry = data.get("retryAfterSeconds", 30)
            lines.append(f"\n*Retryable: wait {retry}s before retrying.*")
        return "\n".join(lines)

    # Empty result
    if data.get("query_status") == "no_data_found":
        lines.append(f"**No results found**: {data.get('message', '')}")
        if data.get("suggestions"):
            lines.append("\n**Suggestions:**")
            for s in data["suggestions"]:
                lines.append(f"- {s}")
        return "\n".join(lines)

    source = data.get("source", "unknown")
    query = data.get("query", "")
    if query:
        lines.append(f"## Results for: {query}")
    lines.append(f"*Source: {source}*\n")

    # Handle result lists
    results = data.get("results", [])
    if results:
        total = data.get("result_count", data.get("total_count", len(results)))
        lines.append(f"Found **{total}** results:\n")
        for i, r in enumerate(results, 1):
            title = r.get("title", r.get("case_name", "Untitled"))
            lines.append(f"### {i}. {title}")
            for key, val in r.items():
                if key in ("title", "case_name") or not val:
                    continue
                if key == "url":
                    lines.append(f"- **Link**: {val}")
                elif key == "snippet" or key == "abstract":
                    lines.append(f"- {val}")
                else:
                    lines.append(f"- **{key}**: {val}")
            lines.append("")
    # Handle structure/content responses
    elif "structure" in data:
        lines.append("### CFR Structure\n")
        for part in data["structure"]:
            ident = part.get("identifier", "")
            label = part.get("label", "")
            desc = part.get("label_description", "")
            lines.append(f"- **{ident}** {label}: {desc}")
    elif "content" in data:
        lines.append(f"### CFR Title {data.get('cfr_title', '')} § {data.get('section', '')}\n")
        lines.append(data["content"][:5000])
    elif "opinion_text" in data:
        lines.append(f"### {data.get('case_name', 'Case')}\n")
        lines.append(f"- **Court**: {data.get('court', '')}")
        lines.append(f"- **Date Filed**: {data.get('date_filed', '')}")
        lines.append(f"- **Docket**: {data.get('docket_number', '')}")
        if data.get("judges"):
            lines.append(f"- **Judges**: {data['judges']}")
        if data.get("content_incomplete"):
            lines.append("\n*Warning: Opinion text may be incomplete.*")
        if data.get("opinion_text"):
            lines.append(f"\n#### Opinion Text\n\n{data['opinion_text'][:5000]}")
    elif "judgment_text" in data:
        lines.append(f"### {data.get('case_name', 'Case')}\n")
        lines.append(f"- **Court**: {data.get('court', '')}")
        lines.append(f"- **Date**: {data.get('date', '')}")
        lines.append(f"- **Citation**: {data.get('citation', '')}")
        if data.get("coram"):
            lines.append(f"- **Coram**: {data['coram']}")
        if data.get("content_incomplete"):
            lines.append("\n*Warning: Judgment text may be incomplete.*")
        if data.get("judgment_text"):
            lines.append(f"\n#### Judgment Text\n\n{data['judgment_text'][:5000]}")
    elif "full_text" in data:
        lines.append(f"### {data.get('title', 'Document')}\n")
        if data.get("metadata"):
            lines.append(f"*{data['metadata']}*\n")
        if data.get("content_incomplete"):
            lines.append("*Warning: Document content appears incomplete.*\n")
        if data.get("full_text"):
            lines.append(data["full_text"][:5000])

    return "\n".join(lines) if lines else json.dumps(data, ensure_ascii=False, indent=2)


async def _unified_westlaw_with_fallback(query: str, limit: int) -> dict[str, Any]:
    """Try Westlaw Classic, fallback to CourtListener for unified_search."""
    try:
        data = await westlaw_classic.search(query=query, limit=limit)
        if data.get("results") and not data.get("error"):
            return data
        logger.warning("Westlaw Classic empty/error in unified search — fallback to CourtListener")
    except Exception as e:
        logger.warning(
            "Westlaw Classic failed in unified search (%s) — fallback to CourtListener", e
        )

    data = await courtlistener.search_opinions(query=query, limit=limit)
    data["source"] = "courtlistener (westlaw_classic fallback)"
    return data


# ── Tool 1: WestLaw Classic Search ──────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_classic_search(
    query: str,
    content_type: str | None = None,
    jurisdiction: str | None = None,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Search WestLaw Classic — global legal resources via institutional access.

    Tries Westlaw Classic first (institutional subscription). If unavailable,
    falls back to CourtListener (US case law, free).

    - query: Search query (supports Westlaw syntax like 'copyright /s "fair use"').
    - content_type: Filter — 'cases', 'statutes', 'regulations', 'secondary', or None for all.
    - jurisdiction: e.g. 'US-FED', 'US-CA', 'EU', 'UK'.
    - limit: Max results (1-100).
    - response_format: 'markdown' or 'json'.
    Auth: Requires institutional Westlaw subscription. Falls back to CourtListener if unavailable.
    """
    fmt = ResponseFormat(response_format)

    with tool_tracker("westlaw_classic_search", {"query": query[:80]}) as t:
        try:
            data = await westlaw_classic.search(
                query=query,
                content_type=content_type,
                jurisdiction=jurisdiction,
                limit=limit,
            )
            if data.get("results") and not data.get("error"):
                t.set_result(data)
                return _format(data, fmt)
            westlaw_error = data.get("error", "no results")
            logger.warning(
                "Westlaw Classic failed (%s) — falling back to CourtListener", westlaw_error
            )
        except Exception as e:
            logger.warning("Westlaw Classic exception (%s) — falling back to CourtListener", e)

        data = await courtlistener.search_opinions(
            query=query, court=jurisdiction, limit=min(limit, 100)
        )
        if "error" not in data:
            data["_notice"] = (
                "Westlaw Classic was unavailable — results from CourtListener (fallback). "
                "For broader legal search, use westlaw_unified_search."
            )
            data["source"] = "courtlistener (westlaw_classic fallback)"
        t.set_result(data)
    return _format(data, fmt)


# ── Tool 2: WestLaw Classic Get Document ─────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_classic_get_document(
    doc_url: str,
    include_full_text: bool = True,
) -> str:
    """Retrieve a specific document from WestLaw Classic or CourtListener.

    - doc_url: Full document URL (Westlaw or CourtListener).
    - include_full_text: Whether to extract full document text (default True).
    Note: Returns content_incomplete warning if full text is unusually short (<100 chars).
    Auth: Institutional Westlaw subscription required for Westlaw URLs.
    """
    import re

    with tool_tracker("westlaw_classic_get_document", {"url": doc_url[:80]}) as t:
        # CourtListener URLs — fetch directly via API
        if "courtlistener.com" in doc_url:
            cluster_match = re.search(r"/opinion/(\d+)/", doc_url)
            if cluster_match:
                cluster_id = cluster_match.group(1)
                data = await courtlistener.get_opinion_cluster(cluster_id)
                t.set_result(data)
                return _format(data, ResponseFormat.MARKDOWN)

        # Westlaw URLs — try Playwright first
        if "westlaw" in doc_url.lower():
            try:
                data = await westlaw_classic.get_document(
                    doc_url=doc_url,
                    include_full_text=include_full_text,
                )
                # Content completeness check
                full_text = data.get("full_text", "")
                if full_text and len(full_text.strip()) > 100:
                    t.set_result(data)
                    return _format(data, ResponseFormat.MARKDOWN)

                if full_text and len(full_text.strip()) < 100:
                    data["content_incomplete"] = True
                    data["_notice"] = (
                        "Document retrieved but content is unusually short. "
                        "May require institutional access for full text."
                    )
                    t.set_result(data)
                    return _format(data, ResponseFormat.MARKDOWN)

                logger.warning("Westlaw Classic returned empty document — providing alternatives")
            except Exception as e:
                logger.warning("Westlaw Classic document retrieval failed (%s)", e)

            error = make_error(
                "content_incomplete",
                "Could not access Westlaw document (institutional subscription required).",
                source="westlaw_classic",
                suggestions=[
                    "Use westlaw_search_cases to search US case law via CourtListener (free)",
                    "Use westlaw_unified_search to search multiple free legal databases",
                    "Use westlaw_search_legislation for US bills via Congress.gov",
                    "Use westlaw_search_regulations for federal regulations",
                    "Use westlaw_get_cfr_section for Code of Federal Regulations",
                    "Use westlaw_search_eu_law for EU law via EUR-Lex",
                ],
            )
            t.set_result(error)
            return _format(error, ResponseFormat.MARKDOWN)

    return _format(
        make_error(
            "invalid_parameter",
            f"Unsupported document URL: {doc_url}",
            suggestions=["Use a CourtListener or Westlaw URL"],
        ),
        ResponseFormat.MARKDOWN,
    )


# ── Tool 3: Search US Cases (CourtListener) ──────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_search_cases(
    query: str,
    court: str | None = None,
    date_after: str | None = None,
    date_before: str | None = None,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Search US case law via CourtListener — 3,352 courts, RECAP archive.

    - query: Search query for case law.
    - court: Court filter (e.g. 'scotus', 'ca9' for 9th Circuit, 'ca2' for 2nd Circuit).
    - date_after: Cases filed after date (YYYY-MM-DD).
    - date_before: Cases filed before date (YYYY-MM-DD).
    - limit: Max results (1-100).
    - response_format: 'markdown' or 'json'.
    Auth: Optional COURTLISTENER_API_KEY for higher rate limits.
    """
    inp = CaseSearchInput(
        query=query,
        court=court,
        date_after=date_after,
        date_before=date_before,
        limit=limit,
        response_format=ResponseFormat(response_format),
    )
    with tool_tracker("westlaw_search_cases", {"query": query[:80]}) as t:
        data = await courtlistener.search_opinions(
            query=inp.query,
            court=inp.court,
            date_after=inp.date_after,
            date_before=inp.date_before,
            limit=inp.limit,
            offset=inp.offset,
        )
        t.set_result(data)
    return _format(data, inp.response_format)


# ── Tool 4: Get Case Details ───────────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_get_case(
    cluster_id: str | None = None,
    case_name: str | None = None,
    citation: str | None = None,
    doc_url: str | None = None,
) -> str:
    """Get full case details — tries Westlaw Classic, falls back to CourtListener.

    Provide at least one identifier:
    - cluster_id: CourtListener cluster ID (from search results).
    - case_name: e.g. "Roe v. Wade".
    - citation: e.g. "410 U.S. 113".
    - doc_url: Direct Westlaw or CourtListener URL.
    Auth: Westlaw Classic requires institutional subscription.
    """
    import re

    try:
        CaseGetInput(cluster_id=cluster_id, case_name=case_name, citation=citation, doc_url=doc_url)
    except ValueError as e:
        return _format(
            make_error("invalid_parameter", str(e), source="westlaw"),
            ResponseFormat.MARKDOWN,
        )

    with tool_tracker("westlaw_get_case", {"case_name": case_name, "citation": citation}) as t:
        # Direct URL retrieval
        if doc_url:
            if "courtlistener.com" in doc_url:
                cluster_match = re.search(r"/opinion/(\d+)/(?:[^/]+/)?", doc_url)
                if cluster_match:
                    cluster_id = cluster_match.group(1)
            else:
                data = await westlaw_classic.get_document(doc_url=doc_url, include_full_text=True)
                if data.get("full_text") and len(data["full_text"].strip()) > 100:
                    t.set_result(data)
                    return _format(data, ResponseFormat.MARKDOWN)

        # Resolve cluster_id → case_name via CourtListener
        if cluster_id and not case_name and not citation:
            try:
                cl_data = await courtlistener.search_opinions(
                    query=f"cluster_id:{cluster_id}", limit=1
                )
                results = cl_data.get("results", [])
                if results:
                    case_name = results[0].get("title", "")
                    raw_cite = results[0].get("citation", "")
                    citation = (
                        raw_cite[0] if isinstance(raw_cite, list) and raw_cite else str(raw_cite)
                    )
            except Exception:
                pass

        query = citation or case_name or ""
        if not query:
            error = make_empty_result(
                source="westlaw",
                message=f"Could not resolve cluster ID '{cluster_id}' to a case name.",
                suggestions=[
                    "Use case_name parameter directly (e.g. 'Roe v. Wade')",
                    "Use citation parameter (e.g. '410 U.S. 113')",
                ],
            )
            t.set_result(error)
            return _format(error, ResponseFormat.MARKDOWN)

        # Search Westlaw Classic
        data = None
        try:
            data = await westlaw_classic.search(query=query, limit=3)
            if data.get("results") and not data.get("error"):
                first = data["results"][0]
                if first.get("url"):
                    doc_data = await westlaw_classic.get_document(
                        doc_url=first["url"], include_full_text=True
                    )
                    if doc_data.get("full_text") and len(doc_data["full_text"].strip()) > 100:
                        t.set_result(doc_data)
                        return _format(doc_data, ResponseFormat.MARKDOWN)
                data["_notice"] = "Full text extraction failed — showing search summary."
                t.set_result(data)
                return _format(data, ResponseFormat.MARKDOWN)
            westlaw_error = data.get("error", "no results")
        except Exception as e:
            westlaw_error = str(e)

        # Westlaw Classic failed — fallback to CourtListener
        logger.warning(
            "Westlaw Classic get_case failed for '%s' (%s) — falling back to CourtListener",
            query,
            westlaw_error,
        )
        cl_data = await courtlistener.search_opinions(query=query, limit=3)
        cl_results = cl_data.get("results", [])
        if cl_results:
            cl_data["_notice"] = (
                "Westlaw Classic was unavailable — results from CourtListener (fallback). "
                "For full Westlaw text, retry after the session warms up."
            )
            cl_data["source"] = "courtlistener (get_case fallback)"
            t.set_result(cl_data)
            return _format(cl_data, ResponseFormat.MARKDOWN)

        error = make_empty_result(
            query=query,
            source="westlaw",
            message=f"Case not found: {query}",
            suggestions=[
                "Use westlaw_classic_search for broader search",
                "Use westlaw_search_cases for CourtListener (free)",
            ],
        )
        t.set_result(error)
    return _format(error, ResponseFormat.MARKDOWN)


# ── Tool 5: Search Legislation (Congress.gov) ────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_search_legislation(
    query: str,
    congress: int | None = None,
    bill_type: str | None = None,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Search US legislation via Congress.gov API.

    Searches by matching your query against bill titles (Congress.gov API does not
    support full-text search). For broader legal text search, use westlaw_unified_search.

    - query: Keywords to match against bill titles.
    - congress: Congress number (e.g. 118 for 118th Congress, 119 for current).
    - bill_type: One of: 'hr' (House), 's' (Senate), 'hjres', 'sjres', 'hconres', 'sconres'.
    - limit: Max results (1-100).
    - response_format: 'markdown' or 'json'.
    Auth: REQUIRED — set CONGRESS_API_KEY env var. Free key at https://api.congress.gov/sign_up/
    Related: Use westlaw_search_regulations for federal regulations (no key needed).
    """
    fmt = ResponseFormat(response_format)

    with tool_tracker("westlaw_search_legislation", {"query": query[:80]}) as t:
        data = await congress_client.search_bills(
            query=query, congress=congress, bill_type=bill_type, limit=limit
        )
        t.set_result(data)
    return _format(data, fmt)


# ── Tool 6: Search Regulations (Federal Register) ────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_search_regulations(
    query: str,
    doc_type: str | None = None,
    agency: str | None = None,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Search Federal Register — regulations, executive orders, notices.

    - query: Search query.
    - doc_type: One of: 'RULE' (final rule), 'PRORULE' (proposed rule),
      'NOTICE', 'PRESDOCU' (executive orders/presidential documents).
    - agency: Agency slug (e.g. 'environmental-protection-agency', 'securities-and-exchange-commission').
    - limit: Max results (1-100).
    - response_format: 'markdown' or 'json'.
    Auth: None required (free API).
    """
    inp = RegulationSearchInput(
        query=query,
        doc_type=doc_type,
        agency=agency,
        limit=limit,
        response_format=ResponseFormat(response_format),
    )
    with tool_tracker("westlaw_search_regulations", {"query": query[:80]}) as t:
        data = await federal_register.search_documents(
            query=inp.query,
            doc_type=inp.doc_type,
            agency=inp.agency,
            limit=inp.limit,
            offset=inp.offset,
        )
        t.set_result(data)
    return _format(data, inp.response_format)


# ── Tool 7: Get CFR Section (eCFR) ──────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_get_cfr_section(
    title: int,
    part: str | None = None,
    section: str | None = None,
    query: str | None = None,
) -> str:
    """Get Code of Federal Regulations (CFR) sections via eCFR.

    Two modes:
    1. **Exact section lookup**: Provide title + section (e.g. title=45, section='164.502')
       to get the full text of a specific CFR section.
    2. **Text search**: Provide title + query to search for matching sections.
    3. **Browse structure**: Provide title only (optionally + part) to see table of contents.

    - title: CFR title number (1-50). Common: 21=Food&Drug, 26=IRS, 42=PublicHealth, 45=HHS.
    - part: Part number (e.g. '164' for HIPAA Privacy Rule).
    - section: Exact section number — use dot notation: '164.502' (not '164-502').
    - query: Text search within the CFR title.
    Auth: None required (free API).
    Known limitation: eCFR full-text endpoint is deprecated; sections are retrieved via search API excerpts.
    """
    inp = CFRSectionInput(title=title, part=part, section=section, query=query)
    with tool_tracker("westlaw_get_cfr_section", {"title": title, "section": section}) as t:
        data = await ecfr.search_cfr(
            title=inp.title,
            query=inp.query,
            part=inp.part,
            section=inp.section,
        )
        t.set_result(data)
    return _format(data, ResponseFormat.MARKDOWN)


# ── Tool 8: Search EU Law (EUR-Lex) ─────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_search_eu_law(
    query: str,
    doc_type: str | None = None,
    year: int | None = None,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Search EU law — regulations, directives, decisions via EUR-Lex.

    Searches EUR-Lex (web + SPARQL) for EU legal documents.

    - query: Search query for EU law. Use full terms (e.g. 'artificial intelligence' not 'AI Act').
    - doc_type: One of: 'regulation', 'directive', 'decision'. None = all types.
    - year: Publication year filter (e.g. 2024).
    - limit: Max results (1-100).
    - response_format: 'markdown' or 'json'.
    Auth: None required (free API).
    Note: Returns search_methods_tried field showing which EUR-Lex APIs were queried.
    """
    fmt = ResponseFormat(response_format)

    with tool_tracker("westlaw_search_eu_law", {"query": query[:80]}) as t:
        data = await eurlex.search_eu_law(
            query=query,
            doc_type=doc_type,
            year=year,
            limit=limit,
            offset=0,
        )
        t.set_result(data)
    return _format(data, fmt)


# ── Tool 9: Unified Search ────────────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_unified_search(
    query: str,
    sources: str | None = None,
    limit: int = 10,
    response_format: str = "markdown",
) -> str:
    """Cross-source unified legal search — search multiple legal databases at once.

    Queries selected sources in parallel and merges results.

    - query: Search query across all sources.
    - sources: Comma-separated list. Available: 'westlaw' (institutional), 'cases' (CourtListener),
      'legislation' (Congress.gov, needs key), 'regulations' (Federal Register),
      'eu' (EUR-Lex), 'taiwan' (Taiwan Judicial Yuan), 'sec' (SEC EDGAR),
      'singapore' (eLitigation). Default: cases,legislation,regulations,eu.
    - limit: Max results per source (1-50).
    - response_format: 'markdown' or 'json'.
    """
    import asyncio

    inp = UnifiedSearchInput(
        query=query,
        sources=sources,
        limit=min(limit, 50),
        response_format=ResponseFormat(response_format),
    )

    if inp.sources:
        requested = {s.strip().lower() for s in inp.sources.split(",")}
    else:
        requested = {"cases", "legislation", "regulations", "eu"}

    tasks = {}
    per_source_limit = min(inp.limit, 10)

    if "westlaw" in requested:
        tasks["westlaw_classic"] = _unified_westlaw_with_fallback(inp.query, per_source_limit)
    if "cases" in requested:
        tasks["courtlistener"] = courtlistener.search_opinions(
            query=inp.query, limit=per_source_limit
        )
    if "legislation" in requested:
        tasks["congress_gov"] = congress_client.search_bills(
            query=inp.query, limit=per_source_limit
        )
    if "regulations" in requested:
        tasks["federal_register"] = federal_register.search_documents(
            query=inp.query, limit=per_source_limit
        )
    if "eu" in requested:
        tasks["eurlex"] = eurlex.search_eu_law(query=inp.query, limit=per_source_limit)
    if "taiwan" in requested:
        tasks["taiwan_judicial"] = taiwan_judicial.search_judgments(
            query=inp.query, limit=per_source_limit
        )
    if "sec" in requested:
        tasks["sec_edgar"] = sec_edgar.search_filings(
            company=inp.query, limit=per_source_limit
        )
    if "singapore" in requested:
        tasks["singapore_elit"] = singapore_elit.search_cases(
            query=inp.query, limit=per_source_limit
        )

    if not tasks:
        return _format(
            make_error(
                "invalid_parameter",
                "No valid sources specified. Available: westlaw, cases, legislation, regulations, eu, taiwan, sec, singapore",
                parameter="sources",
            ),
            inp.response_format,
        )

    with tool_tracker(
        "westlaw_unified_search", {"query": query[:80], "sources": list(tasks.keys())}
    ) as t:
        keys = list(tasks.keys())
        raw_results = await asyncio.gather(*tasks.values(), return_exceptions=True)

        merged: dict[str, Any] = {
            "query": inp.query,
            "source": "unified",
            "sources_searched": keys,
            "results_by_source": {},
        }

        for key, result in zip(keys, raw_results):
            if isinstance(result, Exception):
                error_msg = str(result)
                if isinstance(result, ValueError) and "CONGRESS_API_KEY" in error_msg:
                    error_msg = (
                        "Congress.gov API key not configured. "
                        "Get a free key at https://api.congress.gov/sign_up/"
                    )
                elif isinstance(result, httpx.HTTPStatusError):
                    status = result.response.status_code
                    if status == 403:
                        error_msg = "API key not configured or invalid."
                    elif status == 401:
                        error_msg = "Authentication required."
                    elif status == 404:
                        error_msg = "Resource not found."
                merged["results_by_source"][key] = {
                    "source": key,
                    "error": error_msg,
                    "results": [],
                    "query_status": "failed",
                }
            else:
                merged["results_by_source"][key] = result

        t.set_result(merged)

    if inp.response_format == ResponseFormat.JSON:
        return json.dumps(merged, ensure_ascii=False, indent=2)

    # Build unified Markdown
    lines = [f"## Unified Legal Search: {inp.query}\n"]
    for source_key, source_data in merged["results_by_source"].items():
        lines.append(f"### {source_key}")
        if "error" in source_data:
            lines.append(f"*Error: {source_data['error']}*\n")
            continue
        results = source_data.get("results", [])
        if not results:
            lines.append("*No results found.*\n")
            continue
        count = source_data.get("result_count", source_data.get("total_count", len(results)))
        lines.append(f"*{count} results found*\n")
        for i, r in enumerate(results[:5], 1):
            title_text = r.get("title", r.get("case_name", "Untitled"))
            lines.append(f"{i}. **{title_text}**")
            if r.get("url"):
                lines.append(f"   {r['url']}")
            if r.get("snippet") or r.get("abstract"):
                lines.append(f"   _{(r.get('snippet') or r.get('abstract', ''))[:200]}_")
        lines.append("")

    return "\n".join(lines)


# ── Tool 10: Health Check ──────────────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True})
async def westlaw_health_check() -> str:
    """Check health of all legal API connections — API keys, circuit breakers.

    Returns JSON with API key status for each service and circuit breaker states.
    Use this to diagnose authentication or connectivity issues.
    """
    with tool_tracker("westlaw_health_check") as t:
        health: dict[str, Any] = {
            "service": "westlaw_mcp",
            "api_keys": {
                "courtlistener": courtlistener.check_api_key(),
                "congress_gov": congress_client.check_api_key(),
                "taiwan_judicial": taiwan_judicial.check_api_key(),
                "eu_compliance": eu_compliance.check_api_key(),
                "oecd_treaties": oecd_treaties.check_api_key(),
                "sec_edgar": sec_edgar.check_api_key(),
                "singapore_elit": singapore_elit.check_api_key(),
            },
            "circuit_breakers": get_all_breaker_health(),
        }
        t.set_result(health)
    return json.dumps(health, ensure_ascii=False, indent=2)


# ── Tool 11: Taiwan Judgment Search ─────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_search_taiwan_judgments(
    query: str,
    court: str | None = None,
    date_range: str | None = None,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Search Taiwan court judgments via Judicial Yuan database (司法院法學資料檢索系統).

    - query: Search keywords (Chinese or English).
    - court: Court filter: 'TPS' (Supreme), 'TPH' (High), 'TPD' (District), 'TPA' (Admin).
    - date_range: Date range 'YYYY-MM-DD,YYYY-MM-DD' (start,end).
    - limit: Max results (1-100).
    - response_format: 'markdown' or 'json'.
    Auth: None required (free, publicly accessible).
    """
    fmt = ResponseFormat(response_format)

    with tool_tracker("westlaw_search_taiwan_judgments", {"query": query[:80]}) as t:
        data = await taiwan_judicial.search_judgments(
            query=query, court=court, date_range=date_range, limit=limit
        )
        t.set_result(data)
    return _format(data, fmt)


# ── Tool 12: Taiwan Statute Lookup ──────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_get_taiwan_statute(
    law_name: str,
    article: str | None = None,
    response_format: str = "markdown",
) -> str:
    """Look up a Taiwan statute by name, optionally a specific article.

    - law_name: Name of the law (e.g., '民法' for Civil Code, '刑法' for Criminal Code,
      '公司法' for Company Act).
    - article: Specific article number (e.g., '184', '339').
    - response_format: 'markdown' or 'json'.
    Auth: None required (free, publicly accessible).
    """
    fmt = ResponseFormat(response_format)

    with tool_tracker("westlaw_get_taiwan_statute", {"law_name": law_name}) as t:
        data = await taiwan_judicial.get_statute(law_name=law_name, article=article)
        t.set_result(data)
    return _format(data, fmt)


# ── Tool 13: Taiwan Interpretation Search ───────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_search_taiwan_interpretations(
    topic: str,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Search Taiwan constitutional interpretations (Judicial Yuan Interpretations).

    - topic: Search topic or keywords.
    - limit: Max results (1-100).
    - response_format: 'markdown' or 'json'.
    Auth: None required (free, publicly accessible).
    """
    fmt = ResponseFormat(response_format)

    with tool_tracker("westlaw_search_taiwan_interpretations", {"topic": topic[:80]}) as t:
        data = await taiwan_judicial.search_interpretations(topic=topic, limit=limit)
        t.set_result(data)
    return _format(data, fmt)


# ── Tool 14: EU Compliance Search ──────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_eu_compliance_search(
    topic: str,
    regulation_type: str | None = None,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Search EU regulations with compliance focus — GDPR, AI Act, DSA, DMA, NIS2, DORA.

    Extended EUR-Lex search focused on compliance obligations, penalties, and scope.

    - topic: Search topic (e.g., 'data protection', 'artificial intelligence', 'cybersecurity').
    - regulation_type: Filter: 'regulation', 'directive', 'decision', 'delegated', 'implementing'.
    - limit: Max results (1-100).
    - response_format: 'markdown' or 'json'.
    Auth: None required (free API).
    """
    fmt = ResponseFormat(response_format)

    with tool_tracker("westlaw_eu_compliance_search", {"topic": topic[:80]}) as t:
        data = await eu_compliance.search_regulations(
            topic=topic, regulation_type=regulation_type, limit=limit
        )
        t.set_result(data)
    return _format(data, fmt)


# ── Tool 15: EU Compliance Get Article ──────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_eu_compliance_article(
    regulation_id: str,
    article_num: str,
) -> str:
    """Get a specific article from an EU regulation (GDPR, AI Act, DSA, etc.).

    - regulation_id: CELEX number or short name. Short names: 'GDPR', 'AI_ACT', 'DSA',
      'DMA', 'EPRIVACY_DIRECTIVE', 'DATA_ACT', 'DATA_GOVERNANCE_ACT', 'NIS2', 'DORA',
      'CYBER_RESILIENCE_ACT'. Or full CELEX like '32016R0679'.
    - article_num: Article number (e.g., '6', '17', '83').
    Auth: None required (free API).
    """
    with tool_tracker("westlaw_eu_compliance_article", {"regulation_id": regulation_id, "article": article_num}) as t:
        data = await eu_compliance.get_article(
            regulation_id=regulation_id, article_num=article_num
        )
        t.set_result(data)
    return _format(data, ResponseFormat.MARKDOWN)


# ── Tool 16: EU Compliance Compare Regulations ───────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_eu_compliance_compare(
    reg1: str,
    reg2: str,
) -> str:
    """Compare two EU regulations — scope, obligations, penalties, timeline.

    - reg1: First regulation (CELEX or short name like 'GDPR', 'AI_ACT', 'DSA').
    - reg2: Second regulation (CELEX or short name like 'DMA', 'NIS2', 'DORA').
    Auth: None required (free API).
    """
    with tool_tracker("westlaw_eu_compliance_compare", {"reg1": reg1, "reg2": reg2}) as t:
        data = await eu_compliance.compare_regulations(reg1=reg1, reg2=reg2)
        t.set_result(data)
    return _format(data, ResponseFormat.MARKDOWN)


# ── Tool 17: OECD Get Treaty ───────────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_oecd_get_treaty(
    country1: str,
    country2: str,
) -> str:
    """Get bilateral tax treaty between two countries via OECD database.

    Returns withholding rates, PE thresholds, capital gains rules, tie-breaker rules,
    and MLI coverage status.

    - country1: First country ISO code (e.g., 'US', 'TW', 'SG', 'HK').
    - country2: Second country ISO code (e.g., 'GB', 'JP', 'DE', 'NL').
    Auth: Optional OECD_API_KEY for extended access.
    """
    with tool_tracker("westlaw_oecd_get_treaty", {"country1": country1, "country2": country2}) as t:
        data = await oecd_treaties.get_treaty(country1=country1, country2=country2)
        t.set_result(data)
    return _format(data, ResponseFormat.MARKDOWN)


# ── Tool 18: OECD Model Convention ──────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_oecd_model_convention(
    article: str,
) -> str:
    """Search OECD Model Tax Convention by article number or topic.

    Returns article text with paragraph details and related articles.

    - article: Article number (e.g., '5' for PE, '7' for Business Profits,
      '10' for Dividends, '13' for Capital Gains, '15' for Employment Income)
      or topic keyword.
    Auth: Optional OECD_API_KEY for extended access.
    """
    with tool_tracker("westlaw_oecd_model_convention", {"article": article}) as t:
        data = await oecd_treaties.search_model_convention(article=article)
        t.set_result(data)
    return _format(data, ResponseFormat.MARKDOWN)


# ── Tool 19: OECD Commentary ──────────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_oecd_commentary(
    article: str,
) -> str:
    """Get OECD Model Tax Convention Commentary for a specific article.

    Returns commentary paragraphs, key observations, reservations, and
    observations by non-member countries.

    - article: Article number (e.g., '5', '7', '10', '13', '15').
    Auth: Optional OECD_API_KEY for extended access.
    """
    with tool_tracker("westlaw_oecd_commentary", {"article": article}) as t:
        data = await oecd_treaties.get_commentary(article=article)
        t.set_result(data)
    return _format(data, ResponseFormat.MARKDOWN)


# ── Tool 20: OECD MLI Status ───────────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_oecd_mli_status(
    country: str,
) -> str:
    """Check MLI (Multilateral Instrument) status for a country.

    Returns signatory status, ratification date, covered tax agreements,
    reservations, and opted articles.

    - country: Country ISO code (e.g., 'US', 'SG', 'TW', 'GB', 'JP').
    Auth: Optional OECD_API_KEY for extended access.
    """
    with tool_tracker("westlaw_oecd_mli_status", {"country": country}) as t:
        data = await oecd_treaties.check_mli_status(country=country)
        t.set_result(data)
    return _format(data, ResponseFormat.MARKDOWN)


# ── Tool 21: SEC EDGAR Search Filings ──────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_search_sec_filings(
    company: str | None = None,
    filing_type: str | None = None,
    date_range: str | None = None,
    cik: str | None = None,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Search SEC EDGAR filings — 10-K, 10-Q, 8-K, S-1, proxy statements.

    - company: Company name or ticker symbol (e.g., 'Apple', 'AAPL').
    - filing_type: Filing type (e.g., '10-K', '10-Q', '8-K', 'S-1', 'DEF 14A', '13F-HR').
    - date_range: Date range 'YYYY-MM-DD,YYYY-MM-DD' (start,end).
    - cik: SEC Central Index Key (10-digit number).
    - limit: Max results (1-100).
    - response_format: 'markdown' or 'json'.
    Auth: None required (free). Set SEC_EDGAR_EMAIL env var for compliance.
    Rate limit: 10 requests/second.
    """
    fmt = ResponseFormat(response_format)

    with tool_tracker("westlaw_search_sec_filings", {"company": company}) as t:
        data = await sec_edgar.search_filings(
            company=company, filing_type=filing_type, date_range=date_range, cik=cik, limit=limit
        )
        t.set_result(data)
    return _format(data, fmt)


# ── Tool 22: SEC EDGAR Get Filing ──────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_get_sec_filing(
    accession_number: str,
) -> str:
    """Get a specific SEC filing by accession number.

    - accession_number: SEC accession number (e.g., '0000320193-23-000106').
    Auth: None required (free). Set SEC_EDGAR_EMAIL env var for compliance.
    """
    with tool_tracker("westlaw_get_sec_filing", {"accession": accession_number}) as t:
        data = await sec_edgar.get_filing(accession_number=accession_number)
        t.set_result(data)
    return _format(data, ResponseFormat.MARKDOWN)


# ── Tool 23: SEC EDGAR Full-Text Search ────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_sec_full_text_search(
    query: str,
    filing_type: str | None = None,
    date_range: str | None = None,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Full-text search across SEC EDGAR filing content.

    Searches within the text of SEC filings (not just metadata).

    - query: Full-text search query.
    - filing_type: Filter by filing type (e.g., '10-K', '10-Q', '8-K').
    - date_range: Date range 'YYYY-MM-DD,YYYY-MM-DD' (start,end).
    - limit: Max results (1-100).
    - response_format: 'markdown' or 'json'.
    Auth: None required (free). Set SEC_EDGAR_EMAIL env var for compliance.
    """
    fmt = ResponseFormat(response_format)

    with tool_tracker("westlaw_sec_full_text_search", {"query": query[:80]}) as t:
        data = await sec_edgar.search_full_text(
            query=query, filing_type=filing_type, date_range=date_range, limit=limit
        )
        t.set_result(data)
    return _format(data, fmt)


# ── Tool 24: Singapore Case Search ─────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_search_singapore_cases(
    query: str,
    court: str | None = None,
    date_range: str | None = None,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Search Singapore court judgments via eLitigation.

    - query: Search keywords for case law.
    - court: Court filter: 'SGCA' (Court of Appeal), 'SGHC' (High Court),
      'SGDC' (District Court), 'SGMC' (Magistrate's Court).
    - date_range: Date range 'YYYY-MM-DD,YYYY-MM-DD' (start,end).
    - limit: Max results (1-100).
    - response_format: 'markdown' or 'json'.
    Auth: Optional SINGAPORE_ELIT_API_KEY.
    """
    fmt = ResponseFormat(response_format)

    with tool_tracker("westlaw_search_singapore_cases", {"query": query[:80]}) as t:
        data = await singapore_elit.search_cases(
            query=query, court=court, date_range=date_range, limit=limit
        )
        t.set_result(data)
    return _format(data, fmt)


# ── Tool 25: Singapore Get Judgment ─────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": True})
async def westlaw_get_singapore_judgment(
    case_id: str,
) -> str:
    """Get full judgment text from Singapore eLitigation.

    - case_id: Case identifier — eLitigation ID or neutral citation
      (e.g., '[2024] SGCA 1', '[2023] SGHC 200').
    Auth: Optional SINGAPORE_ELIT_API_KEY.
    """
    with tool_tracker("westlaw_get_singapore_judgment", {"case_id": case_id}) as t:
        data = await singapore_elit.get_judgment(case_id=case_id)
        t.set_result(data)
    return _format(data, ResponseFormat.MARKDOWN)
