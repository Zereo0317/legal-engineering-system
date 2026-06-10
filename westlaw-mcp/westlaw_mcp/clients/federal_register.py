"""Federal Register API v1 client — US regulations, executive orders, notices.

Docs: https://www.federalregister.gov/developers/documentation/api/v1
"""

from __future__ import annotations

import logging
from typing import Any

from ..errors import make_empty_result, make_error, make_success

from .base import api_request, handle_api_error

logger = logging.getLogger(__name__)

BASE_URL = "https://www.federalregister.gov/api/v1"

VALID_DOC_TYPES = frozenset({"RULE", "PRORULE", "NOTICE", "PRESDOCU"})


async def search_documents(
    query: str,
    doc_type: str | None = None,
    agency: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """Search Federal Register documents."""
    # Validate doc_type
    if doc_type:
        doc_type = doc_type.upper()
        if doc_type not in VALID_DOC_TYPES:
            return make_error(
                "invalid_parameter",
                f"Invalid doc_type '{doc_type}'. Must be one of: {', '.join(sorted(VALID_DOC_TYPES))}",
                parameter="doc_type",
                source="federal_register",
            )

    params: dict[str, Any] = {
        "conditions[term]": query,
        "per_page": min(limit, 200),
        "page": (offset // max(limit, 1)) + 1,
        "order": "relevance",
        "fields[]": [
            "title",
            "type",
            "abstract",
            "document_number",
            "publication_date",
            "agencies",
            "html_url",
            "citation",
        ],
    }
    if doc_type:
        params["conditions[type][]"] = doc_type
    if agency:
        params["conditions[agencies][]"] = agency

    try:
        data = await api_request(
            f"{BASE_URL}/documents.json",
            params=params,
            service_name="federal_register",
        )

        results = []
        for doc in data.get("results", [])[:limit]:
            agencies = doc.get("agencies", [])
            agency_names = [a.get("name", "") for a in agencies if isinstance(a, dict)]

            results.append(
                {
                    "title": doc.get("title", ""),
                    "type": doc.get("type", ""),
                    "document_number": doc.get("document_number", ""),
                    "publication_date": doc.get("publication_date", ""),
                    "citation": doc.get("citation", ""),
                    "agencies": ", ".join(agency_names),
                    "abstract": (doc.get("abstract") or "")[:500],
                    "url": doc.get("html_url", ""),
                }
            )

        if not results:
            return make_empty_result(
                query=query,
                source="federal_register",
                message=f"No regulations found for: {query}",
                suggestions=[
                    "Try broader search terms",
                    "Remove doc_type or agency filters",
                    f"Valid doc_types: {', '.join(sorted(VALID_DOC_TYPES))}",
                ],
            )

        return make_success({
            "query": query,
            "source": "federal_register",
            "total_count": data.get("count", len(results)),
            "result_count": len(results),
            "results": results,
        })
    except Exception as e:
        logger.exception("Federal Register search failed: %s", e)
        return handle_api_error(e, source="federal_register")
