import datetime as dt
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict


@dataclass
class RateLimitResult:
    allowed: bool
    retry_after: int


class RateLimiter:
    def __init__(self, max_events: int = 5, window_seconds: int = 10):
        self.max_events = max_events
        self.window = dt.timedelta(seconds=window_seconds)
        self.events: Dict[int, Deque[dt.datetime]] = {}

    def check(self, user_id: int) -> RateLimitResult:
        now = dt.datetime.utcnow()
        dq = self.events.setdefault(user_id, deque())
        while dq and now - dq[0] > self.window:
            dq.popleft()
        if len(dq) >= self.max_events:
            retry = int((self.window - (now - dq[0])).total_seconds())
            return RateLimitResult(allowed=False, retry_after=max(retry, 1))
        dq.append(now)
        return RateLimitResult(allowed=True, retry_after=0)
