"""Circuit breaker for upstream API calls."""

from __future__ import annotations

import threading
import time
from enum import Enum
from typing import Any

from .errors import make_error


class _State(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    def __init__(self, name: str, *, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.name = name
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._state = _State.CLOSED
        self._failure_count = 0
        self._last_failure_time = 0.0
        self._half_open_probe_sent = False
        self._lock = threading.Lock()

    def allow_request(self) -> bool:
        with self._lock:
            self._maybe_half_open()
            if self._state == _State.CLOSED:
                return True
            if self._state == _State.HALF_OPEN and not self._half_open_probe_sent:
                self._half_open_probe_sent = True
                return True
            return False

    def record_success(self) -> None:
        with self._lock:
            self._failure_count = 0
            self._state = _State.CLOSED
            self._half_open_probe_sent = False

    def record_failure(self) -> None:
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            self._half_open_probe_sent = False
            if self._failure_count >= self._failure_threshold:
                self._state = _State.OPEN

    def open_error(self) -> dict[str, Any]:
        return make_error(
            "circuit_open",
            f"{self.name} circuit breaker is OPEN. Retry after {int(self._recovery_timeout)}s.",
            retryable=True,
            retry_after_seconds=int(self._recovery_timeout),
            source=self.name,
        )

    def health(self) -> dict[str, Any]:
        with self._lock:
            self._maybe_half_open()
            return {
                "name": self.name,
                "state": self._state.value,
                "failure_count": self._failure_count,
            }

    def _maybe_half_open(self) -> None:
        if self._state == _State.OPEN and (time.time() - self._last_failure_time) >= self._recovery_timeout:
            self._state = _State.HALF_OPEN


_registry: dict[str, CircuitBreaker] = {}
_lock = threading.Lock()


def get_breaker(name: str, *, failure_threshold: int = 5, recovery_timeout: float = 30.0) -> CircuitBreaker:
    with _lock:
        if name not in _registry:
            _registry[name] = CircuitBreaker(name, failure_threshold=failure_threshold, recovery_timeout=recovery_timeout)
        return _registry[name]


def all_breaker_health() -> dict[str, Any]:
    with _lock:
        return {name: cb.health() for name, cb in _registry.items()}
