"""EU Compliance client — extended EUR-Lex with compliance focus.

Focuses on GDPR, AI Act, Digital Services Act, ePrivacy Regulation,
and other key EU regulatory frameworks.
Docs: https://eur-lex.europa.eu/
"""

from __future__ import annotations

import logging
import os
from typing import Any

from ..errors import from_exception, make_empty_result, make_error, make_success
from .base import api_request, handle_api_error, get_service_breaker

logger = logging.getLogger(__name__)

BASE_URL = "https://eur-lex.europa.eu/EURLexWebService/search"
CELLAR_URL = "https://publications.europa.eu/resource/cellar"

# Key EU regulation CELEX numbers for quick lookup
_REGULATION_CELEX = {
    "GDPR": "32016R0679",
    "AI_ACT": "32024R1689",
    "DSA": "32022R2065",
    "DMA": "32022R1925",
    "EPRIVACY_DIRECTIVE": "32002L0058",
    "DATA_ACT": "32023R2854",
    "DATA_GOVERNANCE_ACT": "32022R0868",
    "NIS2": "32022L2555",
    "DORA": "32022R2554",
    "CYBER_RESILIENCE_ACT": "32024R2847",
}

# Register circuit breaker
_cb = get_service_breaker("eu_compliance")


def _headers() -> dict[str, str]:
    """Default headers for EUR-Lex API."""
    return {
        "Accept": "application/json",
        "Accept-Language": "en",
    }


def check_api_key() -> dict[str, Any]:
    """Check EU Compliance API status (no key required)."""
    return {
        "service": "eu_compliance",
        "api_key_status": "not_required",
        "note": "EUR-Lex APIs are publicly accessible. No API key needed.",
    }


async def search_regulations(
    topic: str,
    regulation_type: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Search EU regulations with compliance focus.

    Args:
        topic: Search topic (e.g., 'data protection', 'artificial intelligence',
               'digital services', 'cybersecurity').
        regulation_type: Filter by type: 'regulation', 'directive', 'decision',
                        'delegated', 'implementing'. None = all.
        limit: Maximum results to return.
    """
    params: dict[str, Any] = {
        "text": topic,
        "page": 1,
        "pageSize": min(limit, 50),
        "type": "act",
        "sortBy": "relevance",
    }
    if regulation_type:
        type_map = {
            "regulation": "REG",
            "directive": "DIR",
            "decision": "DEC",
            "delegated": "DELREG",
            "implementing": "IMPLREG",
        }
        params["subtype"] = type_map.get(regulation_type.lower(), regulation_type.upper())

    try:
        data = await api_request(
            BASE_URL,
            headers=_headers(),
            params=params,
            service_name="eu_compliance",
        )
        results = []
        for item in data.get("results", data.get("data", []))[:limit]:
            celex = item.get("celex", item.get("id", ""))
            results.append({
                "title": item.get("title", item.get("name", "")),
                "celex_number": celex,
                "document_type": item.get("type", item.get("document_type", "")),
                "date_published": item.get("date", item.get("datePublished", "")),
                "status": item.get("status", "in_force"),
                "eli": item.get("eli", ""),
                "summary": item.get("summary", item.get("abstract", ""))[:500],
                "url": f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex}" if celex else item.get("url", ""),
            })

        if not results:
            return make_empty_result(
                query=topic,
                source="eu_compliance",
                message=f"No EU regulations found for: {topic}",
                suggestions=[
                    "Try broader terms (e.g., 'data protection' instead of 'GDPR Art.6')",
                    "Use regulation_type filter: 'regulation', 'directive', 'decision'",
                    "Search common frameworks: GDPR, AI Act, DSA, DMA, NIS2, DORA",
                ],
            )

        return make_success({
            "query": topic,
            "source": "eu_compliance",
            "result_count": data.get("totalResults", len(results)),
            "results": results,
        })
    except Exception as e:
        logger.exception("EU Compliance search failed: %s", e)
        return handle_api_error(e, source="eu_compliance")


async def get_article(
    regulation_id: str,
    article_num: str,
) -> dict[str, Any]:
    """Get a specific article from an EU regulation.

    Args:
        regulation_id: CELEX number or short name (e.g., '32016R0679' or 'GDPR').
        article_num: Article number (e.g., '6', '17', '83').
    """
    # Resolve short names to CELEX
    celex = _REGULATION_CELEX.get(regulation_id.upper(), regulation_id)

    endpoint = f"{BASE_URL}/article"
    params: dict[str, Any] = {
        "celex": celex,
        "article": article_num,
    }

    try:
        data = await api_request(
            endpoint,
            headers=_headers(),
            params=params,
            service_name="eu_compliance",
        )

        # Resolve the regulation name from CELEX
        reg_name = regulation_id
        for name, cx in _REGULATION_CELEX.items():
            if cx == celex:
                reg_name = name
                break

        return make_success({
            "source": "eu_compliance",
            "regulation": reg_name,
            "celex_number": celex,
            "article_number": article_num,
            "title": data.get("title", data.get("articleTitle", "")),
            "content": data.get("content", data.get("text", data.get("articleContent", "")))[:10000],
            "recitals_referenced": data.get("recitals", []),
            "url": f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex}#art_{article_num}",
        })
    except Exception as e:
        logger.exception("EU Compliance get_article failed: %s", e)
        return handle_api_error(e, source="eu_compliance")


async def compare_regulations(
    reg1: str,
    reg2: str,
) -> dict[str, Any]:
    """Compare two EU regulations — scope, obligations, penalties, timeline.

    Args:
        reg1: First regulation (CELEX number or short name like 'GDPR', 'AI_ACT').
        reg2: Second regulation (CELEX number or short name like 'DSA', 'DMA').
    """
    celex1 = _REGULATION_CELEX.get(reg1.upper(), reg1)
    celex2 = _REGULATION_CELEX.get(reg2.upper(), reg2)

    try:
        # Fetch metadata for both regulations
        data1 = await api_request(
            f"{BASE_URL}/metadata",
            headers=_headers(),
            params={"celex": celex1},
            service_name="eu_compliance",
        )
        data2 = await api_request(
            f"{BASE_URL}/metadata",
            headers=_headers(),
            params={"celex": celex2},
            service_name="eu_compliance",
        )

        return make_success({
            "source": "eu_compliance",
            "comparison": {
                "regulation_1": {
                    "name": reg1,
                    "celex": celex1,
                    "title": data1.get("title", ""),
                    "type": data1.get("type", ""),
                    "date_adopted": data1.get("dateAdopted", ""),
                    "date_application": data1.get("dateApplication", ""),
                    "scope": data1.get("scope", ""),
                    "penalties": data1.get("penalties", ""),
                    "url": f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex1}",
                },
                "regulation_2": {
                    "name": reg2,
                    "celex": celex2,
                    "title": data2.get("title", ""),
                    "type": data2.get("type", ""),
                    "date_adopted": data2.get("dateAdopted", ""),
                    "date_application": data2.get("dateApplication", ""),
                    "scope": data2.get("scope", ""),
                    "penalties": data2.get("penalties", ""),
                    "url": f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex2}",
                },
            },
        })
    except Exception as e:
        logger.exception("EU Compliance compare_regulations failed: %s", e)
        return handle_api_error(e, source="eu_compliance")
