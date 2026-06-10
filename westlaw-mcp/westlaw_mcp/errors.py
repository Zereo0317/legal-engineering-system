"""Standardised error response helpers for MCP tools."""

from __future__ import annotations

from typing import Any


def make_error(
    code: str,
    message: str,
    *,
    retryable: bool = False,
    retry_after_seconds: int | None = None,
    upstream_status: int | None = None,
    parameter: str | None = None,
    suggestions: list[str] | None = None,
    source: str | None = None,
) -> dict[str, Any]:
    err: dict[str, Any] = {"error": code, "message": message, "retryable": retryable}
    if retry_after_seconds is not None:
        err["retryAfterSeconds"] = retry_after_seconds
    if upstream_status is not None:
        err["upstream_status"] = upstream_status
    if parameter is not None:
        err["parameter"] = parameter
    if suggestions:
        err["suggestions"] = suggestions
    if source:
        err["source"] = source
    return err


def make_empty_result(
    *,
    query: str = "",
    message: str = "No results found.",
    suggestions: list[str] | None = None,
    source: str | None = None,
) -> dict[str, Any]:
    resp: dict[str, Any] = {
        "results": [],
        "total": 0,
        "query_status": "no_data_found",
        "message": message,
    }
    if query:
        resp["query"] = query
    if suggestions:
        resp["suggestions"] = suggestions
    if source:
        resp["source"] = source
    return resp


def make_success(data: dict[str, Any]) -> dict[str, Any]:
    if "query_status" not in data:
        has_data = bool(data.get("results") or data.get("data"))
        data["query_status"] = "success_with_data" if has_data else "no_data_found"
    return data


def from_http_status(status: int, *, source: str = "", detail: str = "") -> dict[str, Any]:
    if status in (401, 403):
        return make_error("auth_invalid", detail or f"HTTP {status}: authentication failed.", source=source)
    if status == 404:
        return make_error("not_found", detail or "Resource not found.", source=source)
    if status == 429:
        return make_error("rate_limited", detail or "Rate limited.", retryable=True, retry_after_seconds=60, source=source)
    if status in (500, 502, 503, 504):
        return make_error("upstream_unavailable", detail or f"HTTP {status}.", retryable=True, retry_after_seconds=30, source=source)
    return make_error("upstream_unavailable", detail or f"HTTP {status}.", source=source)


def from_exception(exc: Exception, *, source: str = "") -> dict[str, Any]:
    import httpx

    if isinstance(exc, httpx.HTTPStatusError):
        return from_http_status(exc.response.status_code, source=source)
    if isinstance(exc, httpx.TimeoutException):
        return make_error("upstream_unavailable", f"{source or 'API'} timed out.", retryable=True, source=source)
    return make_error("internal_error", f"{type(exc).__name__}: {exc}", source=source)
