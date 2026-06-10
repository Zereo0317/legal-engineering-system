"""CourtListener API client — US case law search across 3,352 courts.

Docs: https://www.courtlistener.com/help/api/rest/
"""

from __future__ import annotations

import logging
import os
from typing import Any

from ..errors import from_exception, make_empty_result, make_error, make_success

from .base import api_request, handle_api_error

logger = logging.getLogger(__name__)

BASE_URL = "https://www.courtlistener.com/api/rest/v4"


def _headers() -> dict[str, str]:
    token = os.getenv("COURTLISTENER_API_KEY", "")
    h: dict[str, str] = {"Accept": "application/json"}
    if token:
        h["Authorization"] = f"Token {token}"
    return h


def check_api_key() -> dict[str, Any]:
    """Check CourtListener API key status."""
    token = os.getenv("COURTLISTENER_API_KEY", "")
    return {
        "service": "courtlistener",
        "api_key_status": "configured" if token else "not_configured",
        "note": "CourtListener works without API key but with rate limits. "
                "Get a free key at https://www.courtlistener.com/help/api/",
    }


async def search_opinions(
    query: str,
    court: str | None = None,
    date_after: str | None = None,
    date_before: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """Search CourtListener opinions (case law)."""
    params: dict[str, Any] = {
        "q": query,
        "order_by": "score desc",
        "page_size": min(limit, 50),
    }
    if offset:
        page = (offset // max(limit, 1)) + 1
        params["page"] = page
    if court:
        params["court"] = court
    if date_after:
        params["filed_after"] = date_after
    if date_before:
        params["filed_before"] = date_before

    try:
        data = await api_request(
            f"{BASE_URL}/search/",
            headers=_headers(),
            params=params,
            service_name="courtlistener",
        )
        results = []
        for item in data.get("results", [])[:limit]:
            results.append(
                {
                    "title": item.get("caseName", ""),
                    "citation": item.get("citation", [item.get("citationCount", "")])[0]
                    if isinstance(item.get("citation"), list) and item.get("citation")
                    else str(item.get("citation", "")),
                    "court": item.get("court", ""),
                    "date_filed": item.get("dateFiled", ""),
                    "docket_number": item.get("docketNumber", ""),
                    "snippet": item.get("snippet", "")[:500],
                    "cluster_id": str(item.get("cluster_id", item.get("id", ""))),
                    "url": item.get("absolute_url", ""),
                }
            )

        if not results:
            return make_empty_result(
                query=query,
                source="courtlistener",
                message=f"No case law found for: {query}",
                suggestions=[
                    "Try broader search terms",
                    "Check court filter spelling (e.g. 'scotus', 'ca9')",
                    "Adjust date range if specified",
                ],
            )

        return make_success({
            "query": query,
            "source": "courtlistener",
            "result_count": data.get("count", len(results)),
            "results": results,
        })
    except Exception as e:
        logger.exception("CourtListener search failed: %s", e)
        return handle_api_error(e, source="courtlistener")


async def get_opinion_cluster(cluster_id: str) -> dict[str, Any]:
    """Get a full opinion cluster (case details + opinions)."""
    try:
        data = await api_request(
            f"{BASE_URL}/clusters/{cluster_id}/",
            headers=_headers(),
            service_name="courtlistener",
        )

        # Fetch first opinion text if available
        opinion_text = ""
        sub_opinions = data.get("sub_opinions", [])
        if sub_opinions:
            opinion_url = sub_opinions[0] if isinstance(sub_opinions[0], str) else ""
            if opinion_url:
                try:
                    op_data = await api_request(
                        opinion_url, headers=_headers(), service_name="courtlistener"
                    )
                    opinion_text = (
                        op_data.get("plain_text", "") or op_data.get("html_with_citations", "")
                    )[:10000]
                except Exception:
                    pass

        result = {
            "case_name": data.get("case_name", ""),
            "date_filed": data.get("date_filed", ""),
            "court": data.get("court", ""),
            "docket_number": data.get("docket_number", ""),
            "citations": data.get("citations", []),
            "judges": data.get("judges", ""),
            "opinion_text": opinion_text,
            "source": "courtlistener",
        }

        # Content completeness check
        if opinion_text and len(opinion_text.strip()) < 100:
            result["content_incomplete"] = True
            result["_notice"] = "Opinion text is unusually short — may be truncated."

        return make_success(result)
    except Exception as e:
        logger.exception("CourtListener get cluster failed: %s", e)
        return handle_api_error(e, source="courtlistener")
