"""Singapore eLitigation / Supreme Court Judgments client.

Searches Singapore court judgments via Singapore Law Watch / eLitigation.
Docs: https://www.elitigation.sg/
      https://www.singaporelawwatch.sg/
"""

from __future__ import annotations

import logging
import os
from typing import Any

from ..errors import from_exception, make_empty_result, make_error, make_success
from .base import api_request, handle_api_error, get_service_breaker

logger = logging.getLogger(__name__)

BASE_URL = "https://www.elitigation.sg/api/v1"
SLW_URL = "https://www.singaporelawwatch.sg/api/v1"

# Register circuit breaker
_cb = get_service_breaker("singapore_elit")


def _headers() -> dict[str, str]:
    """Default headers for Singapore eLitigation."""
    token = os.getenv("SINGAPORE_ELIT_API_KEY", "")
    h: dict[str, str] = {"Accept": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def check_api_key() -> dict[str, Any]:
    """Check Singapore eLitigation API status."""
    token = os.getenv("SINGAPORE_ELIT_API_KEY", "")
    return {
        "service": "singapore_elit",
        "api_key_status": "configured" if token else "not_configured",
        "note": "Singapore eLitigation may require registration. "
                "Public judgments are accessible at https://www.elitigation.sg/",
    }


async def search_cases(
    query: str,
    court: str | None = None,
    date_range: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Search Singapore court judgments.

    Args:
        query: Search keywords for case law.
        court: Court filter. Options: 'SGCA' (Court of Appeal), 'SGHC' (High Court),
               'SGDC' (District Court), 'SGMC' (Magistrate's Court),
               'SGIPOS' (IP Office), 'SGITBR' (Income Tax Board of Review).
        date_range: Date range 'YYYY-MM-DD,YYYY-MM-DD' (start,end).
        limit: Maximum results to return.
    """
    params: dict[str, Any] = {
        "q": query,
        "pageSize": min(limit, 50),
        "page": 1,
        "sortBy": "relevance",
    }
    if court:
        params["court"] = court.upper()
    if date_range:
        parts = date_range.split(",")
        if len(parts) == 2:
            params["dateFrom"] = parts[0].strip()
            params["dateTo"] = parts[1].strip()

    try:
        data = await api_request(
            f"{BASE_URL}/judgments/search",
            headers=_headers(),
            params=params,
            service_name="singapore_elit",
        )

        results = []
        for item in data.get("results", data.get("judgments", data.get("data", [])))[:limit]:
            results.append({
                "title": item.get("title", item.get("case_name", "")),
                "citation": item.get("citation", item.get("neutral_citation", "")),
                "court": item.get("court", item.get("court_name", "")),
                "date": item.get("date", item.get("judgment_date", "")),
                "case_number": item.get("case_no", item.get("case_number", "")),
                "coram": item.get("coram", item.get("judges", "")),
                "catchwords": item.get("catchwords", item.get("keywords", ""))[:300],
                "snippet": item.get("snippet", item.get("summary", ""))[:500],
                "url": item.get("url", item.get("link", "")),
            })

        if not results:
            return make_empty_result(
                query=query,
                source="singapore_elit",
                message=f"No Singapore cases found for: {query}",
                suggestions=[
                    "Try different keywords or broader terms",
                    "Check court code: SGCA (Appeal), SGHC (High Court), SGDC (District)",
                    "Use citation format: [2024] SGCA 1, [2024] SGHC 100",
                    "Broaden date range if specified",
                ],
            )

        return make_success({
            "query": query,
            "source": "singapore_elit",
            "result_count": data.get("total", data.get("totalResults", len(results))),
            "results": results,
        })
    except Exception as e:
        logger.exception("Singapore eLitigation search failed: %s", e)
        return handle_api_error(e, source="singapore_elit")


async def get_judgment(
    case_id: str,
) -> dict[str, Any]:
    """Get full judgment text from Singapore eLitigation.

    Args:
        case_id: Case identifier — either eLitigation ID or neutral citation
                 (e.g., '[2024] SGCA 1', 'SGCA-2024-1').
    """
    # Determine endpoint based on case_id format
    endpoint = f"{BASE_URL}/judgments/{case_id}"

    try:
        data = await api_request(
            endpoint,
            headers=_headers(),
            params={"id": case_id},
            service_name="singapore_elit",
        )

        judgment = data.get("judgment", data)
        judgment_text = judgment.get("content", judgment.get("judgment_text", judgment.get("text", "")))

        result = {
            "source": "singapore_elit",
            "case_name": judgment.get("title", judgment.get("case_name", "")),
            "citation": judgment.get("citation", judgment.get("neutral_citation", "")),
            "court": judgment.get("court", ""),
            "date": judgment.get("date", judgment.get("judgment_date", "")),
            "coram": judgment.get("coram", judgment.get("judges", "")),
            "parties": judgment.get("parties", ""),
            "catchwords": judgment.get("catchwords", ""),
            "headnotes": judgment.get("headnotes", judgment.get("holding", ""))[:2000],
            "judgment_text": judgment_text[:10000] if judgment_text else "",
            "url": judgment.get("url", ""),
        }

        # Content completeness check
        if judgment_text and len(judgment_text.strip()) < 100:
            result["content_incomplete"] = True
            result["_notice"] = "Judgment text is unusually short — may require eLitigation access."

        return make_success(result)
    except Exception as e:
        logger.exception("Singapore eLitigation get_judgment failed: %s", e)
        return handle_api_error(e, source="singapore_elit")
