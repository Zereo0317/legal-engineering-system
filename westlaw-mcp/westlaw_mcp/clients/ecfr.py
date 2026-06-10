"""eCFR API client — Electronic Code of Federal Regulations full text.

Supports two query modes:
  1. Exact section lookup: title + section → full text via search API
  2. Text search: title + query → matching sections

Docs: https://www.ecfr.gov/developer/documentation/api/v1
"""

from __future__ import annotations

import logging
import re as _re
from typing import Any

from ..errors import make_empty_result, make_error, make_success

from .base import api_request, handle_api_error

logger = logging.getLogger(__name__)

BASE_URL = "https://www.ecfr.gov/api"

# CFR citation regex: "164.502" or "§ 164.502" or "45/164/164.502"
_CFR_SECTION_RE = _re.compile(r"^§?\s*(\d+(?:\.\d+)*)$")
_CFR_SLASH_RE = _re.compile(r"^(\d+)/(\d+)/(\d+(?:\.\d+)*)$")


async def search_cfr(
    title: int,
    query: str | None = None,
    part: str | None = None,
    section: str | None = None,
) -> dict[str, Any]:
    """Search or retrieve CFR sections.

    Args:
        title: CFR title number (1-50).
        query: Optional text search within the title.
        part: Optional part number filter.
        section: Optional section number filter.
    """
    if not (1 <= title <= 50):
        return make_error(
            "invalid_parameter",
            f"CFR title must be between 1 and 50, got {title}",
            parameter="title",
            source="ecfr",
        )

    try:
        # If a specific section is requested, fetch it directly
        if section:
            return await _get_section(title, section)

        # Use the versioner API for structure, or search API for text
        if query:
            search_query = query
            if part:
                search_query = f"title {title} part {part} {query}"
            else:
                search_query = f"title {title} {query}"

            data = await api_request(
                f"{BASE_URL}/search/v1/results",
                params={"query": search_query, "per_page": 20},
                service_name="ecfr",
            )

            results = []
            for item in data.get("results", []):
                hierarchy = item.get("hierarchy", {})
                item_title = hierarchy.get("title", "")
                if str(item_title) != str(title):
                    continue

                headings = item.get("hierarchy_headings", {})
                heading_parts = [
                    headings.get("title", ""),
                    headings.get("part", ""),
                    headings.get("section", ""),
                ]
                heading_str = " > ".join(h for h in heading_parts if h)

                results.append(
                    {
                        "title_number": title,
                        "hierarchy": heading_str,
                        "section": hierarchy.get("section", ""),
                        "part": hierarchy.get("part", ""),
                        "snippet": (item.get("full_text_excerpt", "") or "")[:500],
                        "starts_on": item.get("starts_on", ""),
                    }
                )

            if not results:
                return make_empty_result(
                    query=query,
                    source="ecfr",
                    message=f"No CFR sections found in Title {title} matching: {query}",
                    suggestions=[
                        "Try broader search terms",
                        f"Browse title structure: westlaw_get_cfr_section(title={title})",
                        "Check if the correct CFR title number is used",
                    ],
                )

            return make_success({
                "query": query,
                "cfr_title": title,
                "source": "ecfr",
                "result_count": len(results),
                "results": results,
            })
        else:
            # Return title/part structure (table of contents)
            url = f"{BASE_URL}/versioner/v1/structure/{_ecfr_date()}/title-{title}.json"
            if part:
                url = f"{BASE_URL}/versioner/v1/structure/{_ecfr_date()}/title-{title}.json?part={part}"

            data = await api_request(url, service_name="ecfr")
            children = data.get("children", data.get("structure", {}).get("children", []))
            parts = []
            for child in children[:30]:
                parts.append(
                    {
                        "type": child.get("type", ""),
                        "identifier": child.get("identifier", ""),
                        "label": child.get("label", ""),
                        "label_description": child.get("label_description", ""),
                    }
                )

            return make_success({
                "cfr_title": title,
                "source": "ecfr",
                "structure": parts,
            })

    except Exception as e:
        logger.exception("eCFR search failed: %s", e)
        return handle_api_error(e, source="ecfr")


async def _get_section(title: int, section: str) -> dict[str, Any]:
    """Fetch a specific CFR section using the search API.

    The versioner /full/ endpoint returns 404 (deprecated or removed),
    so we use the search API to locate the section and return its excerpt.
    """
    # Validate section format
    section_clean = section.removeprefix("§").strip()
    if not _CFR_SECTION_RE.match(section_clean):
        # Check slash format: "45/164/164.502"
        slash_match = _CFR_SLASH_RE.match(section)
        if slash_match:
            section_clean = slash_match.group(3)
        else:
            return make_error(
                "invalid_parameter",
                f"Invalid CFR section format: '{section}'. "
                f"Expected format: '164.502' or '§ 164.502'.",
                parameter="section",
                source="ecfr",
                suggestions=[
                    "Use dot notation: '164.502'",
                    "Or with symbol: '§ 164.502'",
                    "For browsing, omit section and use query parameter instead",
                ],
            )

    try:
        part = section_clean.split(".")[0] if "." in section_clean else section_clean

        # Primary query: search by title and section number
        search_query = f"title {title} section {section_clean}"
        data = await api_request(
            f"{BASE_URL}/search/v1/results",
            params={"query": search_query, "per_page": 10},
            service_name="ecfr",
        )

        # Find exact match
        best_match = None
        for item in data.get("results", []):
            hierarchy = item.get("hierarchy", {})
            if str(hierarchy.get("title", "")) != str(title):
                continue
            item_section = hierarchy.get("section", "")
            normalized = item_section.removeprefix("§").strip()
            if normalized == section_clean or item_section == section_clean:
                best_match = item
                break
            if section_clean in str(item_section) and best_match is None:
                best_match = item

        # Fallback query: try §-prefixed format
        if not best_match:
            data2 = await api_request(
                f"{BASE_URL}/search/v1/results",
                params={"query": f"§{section_clean}", "per_page": 5},
                service_name="ecfr",
            )
            for item in data2.get("results", []):
                hierarchy = item.get("hierarchy", {})
                if str(hierarchy.get("title", "")) == str(title):
                    best_match = item
                    break

        if best_match:
            headings = best_match.get("hierarchy_headings", {})
            heading_str = " > ".join(
                h
                for h in [
                    headings.get("title", ""),
                    headings.get("part", ""),
                    headings.get("subpart", ""),
                    headings.get("section", ""),
                ]
                if h
            )
            content = _re.sub(r"<[^>]+>", "", best_match.get("full_text_excerpt", "") or "")

            return make_success({
                "cfr_title": title,
                "section": section_clean,
                "part": best_match.get("hierarchy", {}).get("part", part),
                "heading": heading_str,
                "source": "ecfr",
                "content": content[:10000],
                "starts_on": best_match.get("starts_on", ""),
            })

        return make_empty_result(
            source="ecfr",
            message=f"Section {section_clean} not found in CFR Title {title}.",
            suggestions=[
                f"Browse title structure: westlaw_get_cfr_section(title={title})",
                f"Search by keyword: westlaw_get_cfr_section(title={title}, query='...')",
                "Check the section number format (e.g. '164.502' not '164-502')",
            ],
        )
    except Exception as e:
        logger.exception("eCFR get section failed: %s", e)
        return handle_api_error(e, source="ecfr")


def _ecfr_date() -> str:
    """Return 'current' for the eCFR versioner API (always latest available)."""
    return "current"
