"""EUR-Lex REST API client — European Union law search.

Uses the EUR-Lex search API and CELLAR SPARQL endpoint for EU regulations,
directives, decisions, and other EU legal documents.

Docs: https://eur-lex.europa.eu/content/help/eurlex-content/search-tips.html
"""

from __future__ import annotations

import logging
import re
from typing import Any
from xml.etree import ElementTree

import httpx

from ..errors import make_empty_result, make_error, make_success

from .base import handle_api_error

logger = logging.getLogger(__name__)

# EUR-Lex search URL (returns XML/HTML)
SEARCH_URL = "https://eur-lex.europa.eu/search.html"

# EUR-Lex CELLAR SPARQL endpoint
SPARQL_URL = "https://publications.europa.eu/webapi/rdf/sparql"

VALID_DOC_TYPES = frozenset({"regulation", "directive", "decision"})


async def search_eu_law(
    query: str,
    doc_type: str | None = None,
    year: int | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """Search EU legislation via EUR-Lex.

    Tries web search first (more reliable), then SPARQL as fallback.
    Returns structured response with query_status and diagnostic info.
    """
    # Validate doc_type if provided
    if doc_type and doc_type.lower() not in VALID_DOC_TYPES:
        return make_error(
            "invalid_parameter",
            f"Invalid doc_type: '{doc_type}'. Must be one of: {', '.join(sorted(VALID_DOC_TYPES))}",
            parameter="doc_type",
            source="eurlex",
        )

    search_methods_tried: list[str] = []

    try:
        # Primary: web search (more reliable than SPARQL for text queries)
        search_methods_tried.append("eurlex_web_search")
        result = await _web_search(query, doc_type, year, limit)
        if result.get("results"):
            result["search_methods_tried"] = search_methods_tried
            return make_success(result)

        # Fallback: SPARQL for structured queries
        search_methods_tried.append("cellar_sparql")
        results = await _sparql_search(query, doc_type, year, limit, offset)
        if results:
            return make_success({
                "query": query,
                "source": "eurlex",
                "result_count": len(results),
                "results": results,
                "search_methods_tried": search_methods_tried,
            })

        # Both methods returned empty
        return make_empty_result(
            query=query,
            source="eurlex",
            message=f"No EU law results found for: {query}",
            suggestions=[
                "Try broader search terms (e.g. 'artificial intelligence' instead of 'AI Act')",
                "EUR-Lex web and SPARQL searches both returned empty.",
                "Check EUR-Lex directly: https://eur-lex.europa.eu/",
                "Try removing doc_type or year filters for a wider search",
                f"Search methods tried: {', '.join(search_methods_tried)}",
            ],
        )

    except Exception as e:
        logger.exception("EUR-Lex search failed: %s", e)
        return handle_api_error(e, source="eurlex")


async def _sparql_search(
    query: str,
    doc_type: str | None,
    year: int | None,
    limit: int,
    offset: int,
) -> list[dict[str, Any]]:
    """Search EUR-Lex using CELLAR SPARQL endpoint."""
    filters = []
    if doc_type:
        type_uri_map = {
            "regulation": "reg",
            "directive": "dir",
            "decision": "dec",
        }
        if doc_type.lower() in type_uri_map:
            filters.append(
                f'FILTER(CONTAINS(LCASE(STR(?type)), "{type_uri_map[doc_type.lower()]}"))'
            )
    if year:
        filters.append(f"FILTER(YEAR(?date) = {year})")

    filter_clause = "\n    ".join(filters)

    # Escape query for SPARQL string literal AND regex metacharacters
    safe_query = query.replace("\\", "\\\\").replace('"', '\\"')
    safe_query = re.sub(r"([.+*?^${}()|[\]])", r"\\\1", safe_query)

    sparql_query = f"""
    PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT DISTINCT ?work ?title ?celex ?date ?type WHERE {{
        ?work cdm:work_has_expression ?expr .
        ?expr cdm:expression_title ?title .
        ?work cdm:resource_legal_id_celex ?celex .
        OPTIONAL {{ ?work cdm:work_date_document ?date . }}
        OPTIONAL {{ ?work cdm:work_has_resource-type ?type . }}
        FILTER(LANG(?title) = "en")
        FILTER(REGEX(?title, "{safe_query}", "i"))
        {filter_clause}
    }}
    ORDER BY DESC(?date)
    LIMIT {min(limit, 50)}
    OFFSET {offset}
    """

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(
                SPARQL_URL,
                params={"query": sparql_query, "format": "application/sparql-results+xml"},
            )
            resp.raise_for_status()

        root = ElementTree.fromstring(resp.text)
        ns = {"s": "http://www.w3.org/2005/sparql-results#"}

        results = []
        for result_el in root.findall(".//s:result", ns):
            row: dict[str, str] = {}
            for binding in result_el.findall("s:binding", ns):
                name = binding.get("name", "")
                val_el = binding.find("s:literal", ns) or binding.find("s:uri", ns)
                if val_el is not None and val_el.text:
                    row[name] = val_el.text

            if row.get("title"):
                celex = row.get("celex", "")
                results.append(
                    {
                        "title": row["title"][:300],
                        "celex": celex,
                        "date": row.get("date", ""),
                        "type": row.get("type", "").split("/")[-1] if row.get("type") else "",
                        "url": f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex}"
                        if celex
                        else "",
                    }
                )

        return results

    except Exception as e:
        logger.debug("SPARQL search failed, falling back to web: %s", e)
        return []


async def _web_search(
    query: str,
    doc_type: str | None,
    year: int | None,
    limit: int,
) -> dict[str, Any]:
    """Fallback: search EUR-Lex via the web API and return basic results."""
    params: dict[str, Any] = {
        "text": query,
        "qid": "1",
        "type": "quick",
        "DTS_DOM": "EU_LAW",
    }
    if year:
        params["DD_YEAR"] = str(year)

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(SEARCH_URL, params=params)
            resp.raise_for_status()
            html = resp.text

        results = []

        # Strategy 1: EUR-Lex wraps each result in a div.SearchResult block
        blocks = re.findall(
            r'class="SearchResult"(.*?)(?=class="SearchResult"|</div>\s*</div>\s*</div>\s*<!--)',
            html,
            re.DOTALL,
        )

        for i, block in enumerate(blocks):
            if i >= limit:
                break
            title_m = re.search(r'<a[^>]*class="title"[^>]*>([^<]+)', block)
            if not title_m:
                title_m = re.search(r'class="title"[^>]*>([^<]+)', block)
            celex_m = re.search(r"CELEX[:\"]([ A-Z0-9]+)", block)
            href_m = re.search(r'<a[^>]*class="title"[^>]*href="([^"]+)"', block)
            if not href_m:
                href_m = re.search(r'<a[^>]*href="([^"]+)"[^>]*class="title"', block)

            title = title_m.group(1).strip() if title_m else ""
            celex = celex_m.group(1) if celex_m else ""
            href = href_m.group(1).replace("&amp;", "&") if href_m else ""

            if title:
                url = (
                    f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex}"
                    if celex
                    else ""
                )
                if not url and href:
                    url = (
                        f"https://eur-lex.europa.eu/{href.lstrip('./')}"
                        if not href.startswith("http")
                        else href
                    )
                results.append({"title": title[:300], "celex": celex, "url": url})

        # Strategy 2: If SearchResult class not found (EUR-Lex redesign),
        # extract all links pointing to CELEX documents
        if not results:
            celex_links = re.findall(
                r'<a[^>]*href="([^"]*CELEX[^"]*)"[^>]*>([^<]+)</a>',
                html,
            )
            seen: set[str] = set()
            for href_raw, title_raw in celex_links:
                if len(results) >= limit:
                    break
                title = title_raw.strip()
                if len(title) < 5:
                    continue
                celex_m2 = re.search(r"CELEX(?::|%3A)([A-Z0-9]+)", href_raw)
                celex = celex_m2.group(1) if celex_m2 else ""
                dedup_key = celex if celex else f"{title}|{href_raw}"
                if dedup_key in seen:
                    continue
                seen.add(dedup_key)
                href_clean = href_raw.replace("&amp;", "&")
                url = (
                    f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex}"
                    if celex
                    else (
                        f"https://eur-lex.europa.eu/{href_clean.lstrip('./')}"
                        if not href_clean.startswith("http")
                        else href_clean
                    )
                )
                results.append({"title": title[:300], "celex": celex, "url": url})

        return {
            "query": query,
            "source": "eurlex",
            "result_count": len(results),
            "results": results,
            "note": "Results from web search — limited metadata.",
        }

    except Exception as e:
        logger.exception("EUR-Lex web search failed: %s", e)
        return handle_api_error(e, source="eurlex")
