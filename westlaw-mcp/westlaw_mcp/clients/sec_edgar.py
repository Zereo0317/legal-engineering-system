"""SEC EDGAR API client.

Full-text search and filing retrieval from the SEC's EDGAR system.
Docs: https://efts.sec.gov/LATEST/
      https://www.sec.gov/search#/dateRange=custom
"""

from __future__ import annotations

import logging
import os
from typing import Any

from ..errors import from_exception, make_empty_result, make_error, make_success
from .base import api_request, handle_api_error, get_service_breaker

logger = logging.getLogger(__name__)

EFTS_URL = "https://efts.sec.gov/LATEST"
EDGAR_URL = "https://www.sec.gov/cgi-bin/browse-edgar"
SUBMISSIONS_URL = "https://data.sec.gov/submissions"

# Register circuit breaker
_cb = get_service_breaker("sec_edgar")


def _headers() -> dict[str, str]:
    """Default headers — SEC requires User-Agent with contact info."""
    email = os.getenv("SEC_EDGAR_EMAIL", "legal-engineering@example.com")
    return {
        "Accept": "application/json",
        "User-Agent": f"Legal-Engineering-MCP/1.0 ({email})",
    }


def check_api_key() -> dict[str, Any]:
    """Check SEC EDGAR API status."""
    email = os.getenv("SEC_EDGAR_EMAIL", "")
    return {
        "service": "sec_edgar",
        "api_key_status": "not_required",
        "email_configured": "configured" if email else "using_default",
        "note": "SEC EDGAR is free. Set SEC_EDGAR_EMAIL env var for User-Agent compliance. "
                "SEC rate limit: 10 requests/second.",
    }


async def search_filings(
    company: str | None = None,
    filing_type: str | None = None,
    date_range: str | None = None,
    cik: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Search SEC EDGAR filings.

    Args:
        company: Company name or ticker symbol (e.g., 'Apple', 'AAPL').
        filing_type: Filing type (e.g., '10-K', '10-Q', '8-K', 'S-1', 'DEF 14A',
                     '13F-HR', 'SC 13D').
        date_range: Date range 'YYYY-MM-DD,YYYY-MM-DD' (start,end).
        cik: SEC Central Index Key (10-digit number).
        limit: Maximum results to return.
    """
    params: dict[str, Any] = {
        "dateRange": "custom",
    }

    # Build search query
    query_parts = []
    if company:
        query_parts.append(f'companyName:"{company}"')
    if filing_type:
        params["forms"] = filing_type
    if date_range:
        parts = date_range.split(",")
        if len(parts) == 2:
            params["startdt"] = parts[0].strip()
            params["enddt"] = parts[1].strip()
    if cik:
        query_parts.append(f"cik:{cik}")

    search_query = " AND ".join(query_parts) if query_parts else "*"
    params["q"] = search_query
    params["dateRange"] = "custom"
    params["from"] = 0
    params["size"] = min(limit, 50)

    try:
        data = await api_request(
            f"{EFTS_URL}/search-index",
            headers=_headers(),
            params=params,
            service_name="sec_edgar",
        )

        results = []
        hits = data.get("hits", data.get("results", {}))
        items = hits.get("hits", hits.get("data", [])) if isinstance(hits, dict) else hits

        for item in items[:limit]:
            source = item.get("_source", item) if isinstance(item, dict) else {}
            results.append({
                "title": source.get("display_names", [""])[0] if source.get("display_names") else source.get("entity_name", ""),
                "filing_type": source.get("form_type", source.get("file_type", "")),
                "company_name": source.get("entity_name", source.get("company_name", "")),
                "cik": source.get("entity_id", source.get("cik", "")),
                "date_filed": source.get("file_date", source.get("date_filed", "")),
                "accession_number": source.get("accession_no", source.get("accession_number", "")),
                "description": source.get("file_description", "")[:500],
                "url": f"https://www.sec.gov/Archives/edgar/data/{source.get('entity_id', '')}/{source.get('accession_no', '').replace('-', '')}/" if source.get("entity_id") else "",
            })

        if not results:
            return make_empty_result(
                query=company or filing_type or "",
                source="sec_edgar",
                message=f"No SEC filings found for: {company or filing_type or 'query'}",
                suggestions=[
                    "Try company ticker symbol (e.g., 'AAPL' instead of 'Apple Inc.')",
                    "Check filing type format (e.g., '10-K', '10-Q', '8-K')",
                    "Broaden date range",
                    "Use CIK number for exact company match",
                ],
            )

        return make_success({
            "query": company or filing_type or "all",
            "source": "sec_edgar",
            "result_count": hits.get("total", {}).get("value", len(results)) if isinstance(hits, dict) else len(results),
            "results": results,
        })
    except Exception as e:
        logger.exception("SEC EDGAR search_filings failed: %s", e)
        return handle_api_error(e, source="sec_edgar")


async def get_filing(
    accession_number: str,
) -> dict[str, Any]:
    """Get a specific SEC filing by accession number.

    Args:
        accession_number: SEC accession number (e.g., '0000320193-23-000106').
    """
    # Normalize accession number format
    acc_clean = accession_number.replace("-", "")
    acc_formatted = accession_number
    if "-" not in accession_number and len(accession_number) >= 18:
        acc_formatted = f"{accession_number[:10]}-{accession_number[10:12]}-{accession_number[12:]}"

    try:
        # Try EFTS endpoint first
        data = await api_request(
            f"{EFTS_URL}/search-index",
            headers=_headers(),
            params={"q": f'accession_no:"{acc_formatted}"', "size": 1},
            service_name="sec_edgar",
        )

        hits = data.get("hits", data.get("results", {}))
        items = hits.get("hits", []) if isinstance(hits, dict) else []

        if items:
            source = items[0].get("_source", items[0])
            cik = source.get("entity_id", "")
            return make_success({
                "source": "sec_edgar",
                "accession_number": acc_formatted,
                "company_name": source.get("entity_name", ""),
                "cik": cik,
                "filing_type": source.get("form_type", ""),
                "date_filed": source.get("file_date", ""),
                "description": source.get("file_description", ""),
                "filing_url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_clean}/",
                "viewer_url": f"https://www.sec.gov/cgi-bin/viewer?action=view&cik={cik}&type=&dateb=&owner=include&count=40&search_text=&accession={acc_formatted}",
            })

        return make_empty_result(
            query=accession_number,
            source="sec_edgar",
            message=f"Filing not found: {accession_number}",
            suggestions=[
                "Check accession number format: XXXXXXXXXX-YY-ZZZZZZ",
                "Use search_filings to find the correct accession number",
            ],
        )
    except Exception as e:
        logger.exception("SEC EDGAR get_filing failed: %s", e)
        return handle_api_error(e, source="sec_edgar")


async def search_full_text(
    query: str,
    filing_type: str | None = None,
    date_range: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Full-text search across SEC EDGAR filings.

    Args:
        query: Full-text search query (searches within filing content).
        filing_type: Filter by filing type (e.g., '10-K', '10-Q', '8-K').
        date_range: Date range 'YYYY-MM-DD,YYYY-MM-DD' (start,end).
        limit: Maximum results to return.
    """
    params: dict[str, Any] = {
        "q": query,
        "from": 0,
        "size": min(limit, 50),
    }
    if filing_type:
        params["forms"] = filing_type
    if date_range:
        parts = date_range.split(",")
        if len(parts) == 2:
            params["startdt"] = parts[0].strip()
            params["enddt"] = parts[1].strip()

    try:
        data = await api_request(
            f"{EFTS_URL}/search-index",
            headers=_headers(),
            params=params,
            service_name="sec_edgar",
        )

        results = []
        hits = data.get("hits", data.get("results", {}))
        items = hits.get("hits", hits.get("data", [])) if isinstance(hits, dict) else hits

        for item in items[:limit]:
            source = item.get("_source", item) if isinstance(item, dict) else {}
            highlight = item.get("highlight", {})
            snippet = ""
            if highlight:
                snippet_list = highlight.get("file_description", highlight.get("content", []))
                snippet = " ... ".join(snippet_list[:3]) if snippet_list else ""

            results.append({
                "title": source.get("entity_name", ""),
                "filing_type": source.get("form_type", ""),
                "date_filed": source.get("file_date", ""),
                "accession_number": source.get("accession_no", ""),
                "snippet": snippet[:500] or source.get("file_description", "")[:500],
                "url": f"https://www.sec.gov/Archives/edgar/data/{source.get('entity_id', '')}/{source.get('accession_no', '').replace('-', '')}/" if source.get("entity_id") else "",
            })

        if not results:
            return make_empty_result(
                query=query,
                source="sec_edgar",
                message=f"No SEC filings with full-text match for: {query}",
                suggestions=[
                    "Use simpler keywords",
                    "Try search_filings for metadata-based search",
                    "Check filing_type filter if specified",
                ],
            )

        return make_success({
            "query": query,
            "source": "sec_edgar",
            "result_count": hits.get("total", {}).get("value", len(results)) if isinstance(hits, dict) else len(results),
            "results": results,
        })
    except Exception as e:
        logger.exception("SEC EDGAR full-text search failed: %s", e)
        return handle_api_error(e, source="sec_edgar")
