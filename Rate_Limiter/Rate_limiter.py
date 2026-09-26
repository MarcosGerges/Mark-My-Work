from collections import deque
from collections.abc import Callable, Hashable
from threading import Lock
import time
from typing import Protocol


class RateLimitStrategy(Protocol):
	def allow(
		self,
		client_id: Hashable,
		now: float,
		limit: int,
		window_seconds: float,
	) -> bool:
		"""Return whether a request should be accepted."""


class RollingWindowStrategy:
	def __init__(self) -> None:
		self._requests: dict[Hashable, deque[float]] = {}

	def allow(
		self,
		client_id: Hashable,
		now: float,
		limit: int,
		window_seconds: float,
	) -> bool:
		requests = self._requests.setdefault(client_id, deque())
		window_start = now - window_seconds

		while requests and requests[0] <= window_start:
			requests.popleft()

		if len(requests) >= limit:
			return False

		requests.append(now)
		return True


class RateLimiter:
	def __init__(
		self,
		limit: int,
		window_seconds: float,
		strategy: RateLimitStrategy | None = None,
		clock: Callable[[], float] | None = None,
	) -> None:
		if limit <= 0:
			raise ValueError("limit must be greater than zero")
		if window_seconds <= 0:
			raise ValueError("window_seconds must be greater than zero")

		self._limit = limit
		self._window_seconds = window_seconds
		self._strategy = strategy or RollingWindowStrategy()
		self._clock = clock or time.monotonic
		self._lock = Lock()

	def allow(self, client_id: Hashable) -> bool:
		with self._lock:
			return self._strategy.allow(
				client_id,
				self._clock(),
				self._limit,
				self._window_seconds,
			)
