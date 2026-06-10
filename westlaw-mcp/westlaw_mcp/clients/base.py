"""Shared HTTP client and error handling for all legal API clients.

Provides circuit breaker + retry for resilient API calls,
and standardised error responses.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from ..circuit_breaker import get_breaker
from ..errors import from_exception, from_http_status, make_error

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 30.0
MAX_RETRIES = 3
BASE_BACKOFF = 1.0

_RETRYABLE_STATUSES = frozenset({429, 500, 502, 503, 504})

# Named circuit breakers for each upstream
_breakers = {
    "courtlistener": get_breaker("courtlistener", failure_threshold=5, recovery_timeout=30),
    "congress_gov": get_breaker("congress_gov", failure_threshold=3, recovery_timeout=60),
    "federal_register": get_breaker("federal_register", failure_threshold=5, recovery_timeout=30),
    "ecfr": get_breaker("ecfr", failure_threshold=5, recovery_timeout=30),
    "eurlex": get_breaker("eurlex", failure_threshold=5, recovery_timeout=30),
    "westlaw_classic": get_breaker("westlaw_classic", failure_threshold=3, recovery_timeout=60),
}


def get_service_breaker(name: str) -> Any:
    """Get or create a circuit breaker for a named service."""
    if name not in _breakers:
        _breakers[name] = get_breaker(name)
    return _breakers[name]


async def api_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    service_name: str = "legal_api",
) -> dict[str, Any]:
    """Make an async HTTP request with circuit breaker + retry + backoff.

    Returns parsed JSON response or raises on failure.
    """
    cb = _breakers.get(service_name, get_service_breaker(service_name))

    if not cb.allow_request():
        raise _CircuitOpenError(cb.open_error())

    last_error: Exception | None = None

    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        for attempt in range(MAX_RETRIES):
            try:
                resp = await client.request(method, url, headers=headers, params=params)
                resp.raise_for_status()
                cb.record_success()
                return resp.json()

            except httpx.HTTPStatusError as e:
                status = e.response.status_code
                last_error = e

                if status in _RETRYABLE_STATUSES and attempt < MAX_RETRIES - 1:
                    cb.record_failure()
                    wait = BASE_BACKOFF * (2 ** attempt)
                    logger.warning(
                        "%s: HTTP %d on %s (attempt %d/%d, retry in %.1fs)",
                        service_name, status, url, attempt + 1, MAX_RETRIES, wait,
                    )
                    await asyncio.sleep(wait)
                    continue

                if status in _RETRYABLE_STATUSES:
                    cb.record_failure()
                break

            except httpx.TimeoutException as e:
                last_error = e
                cb.record_failure()
                if attempt < MAX_RETRIES - 1:
                    wait = BASE_BACKOFF * (2 ** attempt)
                    logger.warning(
                        "%s: Timeout on %s (attempt %d/%d, retry in %.1fs)",
                        service_name, url, attempt + 1, MAX_RETRIES, wait,
                    )
                    await asyncio.sleep(wait)
                    continue
                break

            except Exception as e:
                last_error = e
                cb.record_failure()
                break

    raise last_error  # type: ignore[misc]


def handle_api_error(e: Exception, source: str = "legal_api") -> dict[str, Any]:
    """Format API errors into a standard error dict for the LLM agent.

    Returns a full structured error dict (not just a string).
    """
    if isinstance(e, _CircuitOpenError):
        return e.error_dict
    return from_exception(e, source=source)


class _CircuitOpenError(Exception):
    """Raised when a circuit breaker is open."""

    def __init__(self, error_dict: dict[str, Any]) -> None:
        self.error_dict = error_dict
        super().__init__(error_dict.get("message", "Circuit breaker open"))


def get_all_breaker_health() -> dict[str, Any]:
    """Return health status for all legal API circuit breakers."""
    return {name: cb.health() for name, cb in _breakers.items()}
