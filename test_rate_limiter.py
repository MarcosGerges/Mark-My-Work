import unittest
from collections.abc import Hashable

from Rate_limiter import RateLimiter


class FakeClock:
	def __init__(self, now: float = 0.0) -> None:
		self.now = now

	def __call__(self) -> float:
		return self.now


class RecordingStrategy:
	def __init__(self) -> None:
		self.calls: list[tuple[Hashable, float, int, float]] = []

	def allow(
		self,
		client_id: Hashable,
		now: float,
		limit: int,
		window_seconds: float,
	) -> bool:
		self.calls.append((client_id, now, limit, window_seconds))
		return True


class RateLimiterTests(unittest.TestCase):
	def test_allows_only_the_configured_number_of_requests(self) -> None:
		limiter = RateLimiter(limit=2, window_seconds=10, clock=FakeClock())

		self.assertTrue(limiter.allow("client-a"))
		self.assertTrue(limiter.allow("client-a"))
		self.assertFalse(limiter.allow("client-a"))

	def test_clients_have_independent_limits(self) -> None:
		limiter = RateLimiter(limit=1, window_seconds=10, clock=FakeClock())

		self.assertTrue(limiter.allow("client-a"))
		self.assertTrue(limiter.allow("client-b"))
		self.assertFalse(limiter.allow("client-a"))

	def test_request_expires_at_exact_rolling_window_boundary(self) -> None:
		clock = FakeClock()
		limiter = RateLimiter(limit=2, window_seconds=10, clock=clock)

		self.assertTrue(limiter.allow("client-a"))
		clock.now = 1
		self.assertTrue(limiter.allow("client-a"))
		clock.now = 9.999
		self.assertFalse(limiter.allow("client-a"))
		clock.now = 10
		self.assertTrue(limiter.allow("client-a"))
		self.assertFalse(limiter.allow("client-a"))

	def test_rejected_request_does_not_extend_the_window(self) -> None:
		clock = FakeClock()
		limiter = RateLimiter(limit=1, window_seconds=10, clock=clock)

		self.assertTrue(limiter.allow("client-a"))
		clock.now = 9
		self.assertFalse(limiter.allow("client-a"))
		clock.now = 10
		self.assertTrue(limiter.allow("client-a"))

	def test_custom_strategy_receives_request_and_configuration(self) -> None:
		clock = FakeClock(now=4.5)
		strategy = RecordingStrategy()
		limiter = RateLimiter(
			limit=3,
			window_seconds=12,
			strategy=strategy,
			clock=clock,
		)

		self.assertTrue(limiter.allow("client-a"))
		self.assertEqual(strategy.calls, [("client-a", 4.5, 3, 12)])

	def test_rejects_non_positive_limit(self) -> None:
		with self.assertRaises(ValueError):
			RateLimiter(limit=0, window_seconds=10)

	def test_rejects_non_positive_window(self) -> None:
		with self.assertRaises(ValueError):
			RateLimiter(limit=1, window_seconds=0)


if __name__ == "__main__":
	unittest.main()