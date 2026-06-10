"""Taiwan Judicial Yuan judgment database client (司法院法學資料檢索系統).

Searches Taiwan court judgments, statutes, and constitutional interpretations.
Docs: https://judgment.judicial.gov.tw/
"""

from __future__ import annotations

import logging
import os
from typing import Any

from ..errors import from_exception, make_empty_result, make_error, make_success
from .base import api_request, handle_api_error, get_service_breaker

logger = logging.getLogger(__name__)

BASE_URL = "https://judgment.judicial.gov.tw/FJUD/data.aspx"
STATUTE_URL = "https://law.moj.gov.tw/api/v1"
INTERPRETATION_URL = "https://cons.judicial.gov.tw/api"

# Register circuit breaker
_cb = get_service_breaker("taiwan_judicial")


def _headers() -> dict[str, str]:
    """Default headers for Taiwan judicial APIs."""
    return {
        "Accept": "application/json",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    }


def check_api_key() -> dict[str, Any]:
    """Check Taiwan Judicial API status (no key required)."""
    return {
        "service": "taiwan_judicial",
        "api_key_status": "not_required",
        "note": "Taiwan Judicial Yuan database is publicly accessible. No API key needed.",
    }


async def search_judgments(
    query: str,
    court: str | None = None,
    date_range: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Search Taiwan court judgments.

    Args:
        query: Search keywords (Chinese or English).
        court: Court filter (e.g., 'TPS' for Supreme Court, 'TPH' for High Court,
               'TPD' for district courts, 'TPA' for Administrative Court).
        date_range: Date range in format 'YYYY-MM-DD,YYYY-MM-DD' (start,end).
        limit: Maximum results to return.
    """
    params: dict[str, Any] = {
        "searchtype": "全文檢索",
        "keyword": query,
        "pagesize": min(limit, 50),
        "page": 1,
    }
    if court:
        params["court"] = court
    if date_range:
        parts = date_range.split(",")
        if len(parts) == 2:
            params["sdate"] = parts[0].strip()
            params["edate"] = parts[1].strip()

    try:
        data = await api_request(
            BASE_URL,
            headers=_headers(),
            params=params,
            service_name="taiwan_judicial",
        )
        results = []
        for item in data.get("results", data.get("data", []))[:limit]:
            results.append({
                "title": item.get("title", item.get("case_name", "")),
                "court": item.get("court", item.get("court_name", "")),
                "case_number": item.get("case_no", item.get("jid", "")),
                "date": item.get("date", item.get("judgment_date", "")),
                "case_type": item.get("case_type", ""),
                "snippet": item.get("summary", item.get("snippet", ""))[:500],
                "url": item.get("url", ""),
            })

        if not results:
            return make_empty_result(
                query=query,
                source="taiwan_judicial",
                message=f"No Taiwan judgments found for: {query}",
                suggestions=[
                    "Try using Traditional Chinese keywords (繁體中文)",
                    "Check court code: TPS (Supreme), TPH (High), TPD (District), TPA (Admin)",
                    "Broaden date range if specified",
                ],
            )

        return make_success({
            "query": query,
            "source": "taiwan_judicial",
            "result_count": data.get("total", len(results)),
            "results": results,
        })
    except Exception as e:
        logger.exception("Taiwan Judicial search failed: %s", e)
        return handle_api_error(e, source="taiwan_judicial")


async def get_statute(
    law_name: str,
    article: str | None = None,
) -> dict[str, Any]:
    """Look up a Taiwan statute by name, optionally a specific article.

    Args:
        law_name: Name of the law (e.g., '民法' for Civil Code, '刑法' for Criminal Code).
        article: Specific article number (e.g., '184', '339').
    """
    params: dict[str, Any] = {
        "LawName": law_name,
    }
    if article:
        params["ArticleNo"] = article

    endpoint = f"{STATUTE_URL}/laws"
    if article:
        endpoint = f"{STATUTE_URL}/laws/articles"

    try:
        data = await api_request(
            endpoint,
            headers=_headers(),
            params=params,
            service_name="taiwan_judicial",
        )

        if article:
            article_data = data.get("article", data)
            return make_success({
                "source": "taiwan_judicial",
                "law_name": law_name,
                "article_number": article,
                "content": article_data.get("content", article_data.get("ArticleContent", "")),
                "effective_date": article_data.get("effective_date", ""),
                "amendment_date": article_data.get("amendment_date", ""),
            })

        law_data = data.get("law", data)
        return make_success({
            "source": "taiwan_judicial",
            "law_name": law_data.get("LawName", law_name),
            "law_category": law_data.get("LawCategory", ""),
            "effective_date": law_data.get("EffectiveDate", ""),
            "amendment_date": law_data.get("AmendmentDate", ""),
            "total_articles": law_data.get("TotalArticles", ""),
            "url": law_data.get("url", ""),
        })
    except Exception as e:
        logger.exception("Taiwan statute lookup failed: %s", e)
        return handle_api_error(e, source="taiwan_judicial")


async def search_interpretations(
    topic: str,
    limit: int = 20,
) -> dict[str, Any]:
    """Search Taiwan constitutional interpretations (Judicial Yuan Interpretations / Constitutional Court rulings).

    Args:
        topic: Search topic or keywords.
        limit: Maximum results to return.
    """
    params: dict[str, Any] = {
        "keyword": topic,
        "pagesize": min(limit, 50),
    }

    try:
        data = await api_request(
            f"{INTERPRETATION_URL}/interpretations",
            headers=_headers(),
            params=params,
            service_name="taiwan_judicial",
        )
        results = []
        for item in data.get("results", data.get("data", []))[:limit]:
            results.append({
                "title": item.get("title", item.get("interpretation_no", "")),
                "interpretation_no": item.get("no", item.get("interpretation_no", "")),
                "date": item.get("date", item.get("interpretation_date", "")),
                "subject": item.get("subject", item.get("holding", ""))[:500],
                "reasoning_summary": item.get("reasoning", item.get("summary", ""))[:500],
                "url": item.get("url", ""),
            })

        if not results:
            return make_empty_result(
                query=topic,
                source="taiwan_judicial",
                message=f"No constitutional interpretations found for: {topic}",
                suggestions=[
                    "Try using Traditional Chinese keywords",
                    "Search by interpretation number (e.g., '釋字第748號')",
                    "Broaden your search terms",
                ],
            )

        return make_success({
            "query": topic,
            "source": "taiwan_judicial",
            "result_count": data.get("total", len(results)),
            "results": results,
        })
    except Exception as e:
        logger.exception("Taiwan interpretations search failed: %s", e)
        return handle_api_error(e, source="taiwan_judicial")
