"""OECD Tax Treaty Database client.

Accesses OECD tax treaty information, Model Tax Convention,
Commentary, and MLI (Multilateral Instrument) status.
Docs: https://www.oecd.org/tax/treaties/
"""

from __future__ import annotations

import logging
import os
from typing import Any

from ..errors import from_exception, make_empty_result, make_error, make_success
from .base import api_request, handle_api_error, get_service_breaker

logger = logging.getLogger(__name__)

BASE_URL = "https://www.oecd.org/tax/treaties/api/v1"
MLI_URL = "https://www.oecd.org/tax/treaties/mli/api/v1"

# Register circuit breaker
_cb = get_service_breaker("oecd_treaties")


def _headers() -> dict[str, str]:
    """Default headers for OECD API."""
    token = os.getenv("OECD_API_KEY", "")
    h: dict[str, str] = {"Accept": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def check_api_key() -> dict[str, Any]:
    """Check OECD API key status."""
    token = os.getenv("OECD_API_KEY", "")
    return {
        "service": "oecd_treaties",
        "api_key_status": "configured" if token else "not_configured",
        "note": "OECD treaty data is partially public. API key provides extended access.",
    }


async def get_treaty(
    country1: str,
    country2: str,
) -> dict[str, Any]:
    """Get bilateral tax treaty between two countries.

    Args:
        country1: First country (ISO 3166-1 alpha-2, e.g., 'US', 'TW', 'SG').
        country2: Second country (ISO 3166-1 alpha-2, e.g., 'GB', 'JP', 'DE').
    """
    params: dict[str, Any] = {
        "country1": country1.upper(),
        "country2": country2.upper(),
    }

    try:
        data = await api_request(
            f"{BASE_URL}/treaties/bilateral",
            headers=_headers(),
            params=params,
            service_name="oecd_treaties",
        )

        treaty = data.get("treaty", data)
        return make_success({
            "source": "oecd_treaties",
            "country1": country1.upper(),
            "country2": country2.upper(),
            "treaty_title": treaty.get("title", ""),
            "signed_date": treaty.get("signed_date", treaty.get("dateSigned", "")),
            "effective_date": treaty.get("effective_date", treaty.get("dateEffective", "")),
            "status": treaty.get("status", ""),
            "withholding_rates": {
                "dividends": treaty.get("wht_dividends", ""),
                "interest": treaty.get("wht_interest", ""),
                "royalties": treaty.get("wht_royalties", ""),
            },
            "pe_threshold": treaty.get("pe_threshold", ""),
            "capital_gains": treaty.get("capital_gains", ""),
            "tie_breaker_rules": treaty.get("tie_breaker", ""),
            "mli_covered": treaty.get("mli_covered", False),
            "protocol_amendments": treaty.get("amendments", []),
            "url": treaty.get("url", ""),
        })
    except Exception as e:
        logger.exception("OECD get_treaty failed: %s", e)
        return handle_api_error(e, source="oecd_treaties")


async def search_model_convention(
    article: str,
) -> dict[str, Any]:
    """Search the OECD Model Tax Convention by article number or topic.

    Args:
        article: Article number (e.g., '5' for PE, '7' for Business Profits,
                 '10' for Dividends, '13' for Capital Gains) or topic keyword.
    """
    params: dict[str, Any] = {
        "article": article,
    }

    try:
        data = await api_request(
            f"{BASE_URL}/model-convention/articles",
            headers=_headers(),
            params=params,
            service_name="oecd_treaties",
        )

        article_data = data.get("article", data)
        return make_success({
            "source": "oecd_treaties",
            "model_convention_version": data.get("version", "2017"),
            "article_number": article_data.get("number", article),
            "title": article_data.get("title", ""),
            "text": article_data.get("text", article_data.get("content", ""))[:10000],
            "paragraphs": article_data.get("paragraphs", []),
            "related_articles": article_data.get("related", []),
            "url": article_data.get("url", ""),
        })
    except Exception as e:
        logger.exception("OECD model convention search failed: %s", e)
        return handle_api_error(e, source="oecd_treaties")


async def get_commentary(
    article: str,
) -> dict[str, Any]:
    """Get OECD Model Tax Convention Commentary for a specific article.

    Args:
        article: Article number (e.g., '5', '7', '10', '13', '15').
    """
    params: dict[str, Any] = {
        "article": article,
    }

    try:
        data = await api_request(
            f"{BASE_URL}/model-convention/commentary",
            headers=_headers(),
            params=params,
            service_name="oecd_treaties",
        )

        commentary = data.get("commentary", data)
        return make_success({
            "source": "oecd_treaties",
            "article_number": article,
            "article_title": commentary.get("article_title", ""),
            "commentary_paragraphs": commentary.get("paragraphs", [])[:50],
            "key_observations": commentary.get("key_observations", []),
            "reservations": commentary.get("reservations", []),
            "observations_by_non_members": commentary.get("non_member_observations", []),
            "last_updated": commentary.get("last_updated", ""),
            "url": commentary.get("url", ""),
        })
    except Exception as e:
        logger.exception("OECD get_commentary failed: %s", e)
        return handle_api_error(e, source="oecd_treaties")


async def check_mli_status(
    country: str,
) -> dict[str, Any]:
    """Check MLI (Multilateral Instrument) status for a country.

    Args:
        country: Country ISO code (e.g., 'US', 'SG', 'TW', 'GB', 'JP').
    """
    params: dict[str, Any] = {
        "country": country.upper(),
    }

    try:
        data = await api_request(
            f"{MLI_URL}/status",
            headers=_headers(),
            params=params,
            service_name="oecd_treaties",
        )

        status_data = data.get("status", data)
        return make_success({
            "source": "oecd_treaties",
            "country": country.upper(),
            "mli_signatory": status_data.get("signatory", False),
            "signature_date": status_data.get("signature_date", ""),
            "ratification_date": status_data.get("ratification_date", ""),
            "entry_into_force": status_data.get("entry_into_force", ""),
            "covered_tax_agreements": status_data.get("covered_agreements", []),
            "reservations": status_data.get("reservations", []),
            "notifications": status_data.get("notifications", []),
            "opted_articles": status_data.get("opted_articles", []),
            "url": status_data.get("url", ""),
        })
    except Exception as e:
        logger.exception("OECD check_mli_status failed: %s", e)
        return handle_api_error(e, source="oecd_treaties")
