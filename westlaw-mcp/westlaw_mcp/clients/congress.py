"""Congress.gov API v3 client — US legislation search.

Docs: https://api.congress.gov/
Free API key: https://api.congress.gov/sign_up/
"""

from __future__ import annotations

import logging
import os
from typing import Any

from ..errors import make_empty_result, make_error, make_success

from .base import api_request, handle_api_error

logger = logging.getLogger(__name__)

BASE_URL = "https://api.congress.gov/v3"


def check_api_key() -> dict[str, Any]:
    """Check Congress.gov API key status."""
    key = os.getenv("CONGRESS_API_KEY", "")
    return {
        "service": "congress_gov",
        "api_key_status": "configured" if key else "not_configured",
        "note": "Get a free API key at https://api.congress.gov/sign_up/",
        "env_var": "CONGRESS_API_KEY",
    }


def _params_with_key(**extra: Any) -> dict[str, Any]:
    key = os.getenv("CONGRESS_API_KEY", "")
    if not key:
        raise _MissingKeyError(
            "CONGRESS_API_KEY environment variable is required. "
            "Get a free API key at https://api.congress.gov/sign_up/"
        )
    params: dict[str, Any] = {"format": "json", "api_key": key}
    params.update({k: v for k, v in extra.items() if v is not None})
    return params


class _MissingKeyError(Exception):
    pass


def _matches_query(bill: dict, query: str) -> bool:
    """Check if a bill title or latest action matches the search query."""
    q = query.lower()
    terms = q.split()
    title = (bill.get("title") or "").lower()
    action = (bill.get("latestAction", {}).get("text") or "").lower()
    text = f"{title} {action}"
    return all(term in text for term in terms)


async def search_bills(
    query: str,
    congress: int | None = None,
    bill_type: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """Search Congress.gov bills with client-side keyword filtering.

    The Congress.gov API v3 /bill endpoint lists bills but does not support
    full-text keyword search. We fetch a large page and filter by matching
    the query against bill titles and latest actions.
    """
    try:
        fetch_limit = min(max(limit * 5, 250), 250)
        params = _params_with_key(limit=fetch_limit, offset=offset)
    except _MissingKeyError:
        return make_error(
            "auth_missing",
            "Congress.gov API key not configured. Cannot search legislation.",
            source="congress_gov",
            suggestions=[
                "Set CONGRESS_API_KEY environment variable",
                "Get a free key at https://api.congress.gov/sign_up/",
                "Use westlaw_search_regulations for federal regulations (no key needed)",
                "Use westlaw_search_cases for case law (no key needed)",
            ],
        )

    if congress and bill_type:
        url = f"{BASE_URL}/bill/{congress}/{bill_type}"
    elif congress:
        url = f"{BASE_URL}/bill/{congress}"
    else:
        url = f"{BASE_URL}/bill"

    try:
        data = await api_request(
            url,
            headers={"Accept": "application/json"},
            params=params,
            service_name="congress_gov",
        )

        bills = data.get("bills", [])
        results = []
        for bill in bills:
            if query and not _matches_query(bill, query):
                continue
            results.append(
                {
                    "title": bill.get("title", ""),
                    "bill_number": bill.get("number", ""),
                    "bill_type": bill.get("type", ""),
                    "congress": bill.get("congress", ""),
                    "origin_chamber": bill.get("originChamber", ""),
                    "latest_action": bill.get("latestAction", {}).get("text", ""),
                    "latest_action_date": bill.get("latestAction", {}).get("actionDate", ""),
                    "url": bill.get("url", ""),
                }
            )
            if len(results) >= limit:
                break

        if not results:
            return make_empty_result(
                query=query,
                source="congress_gov",
                message=f"No legislation found matching: {query}",
                suggestions=[
                    "Try broader or shorter search terms",
                    "Congress.gov search matches against bill titles (not full text)",
                    "Use westlaw_unified_search for broader legal text search",
                    "Check congress number (current: 118th or 119th)",
                    "Try searching without bill_type filter",
                ],
            )

        return make_success(
            {
                "query": query,
                "source": "congress_gov",
                "result_count": len(results),
                "_note": "Filtered by title match (Congress.gov API has no full-text search)",
                "results": results,
            }
        )
    except Exception as e:
        logger.exception("Congress.gov search failed: %s", e)
        return handle_api_error(e, source="congress_gov")
