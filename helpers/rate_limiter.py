import os

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from throttled.fastapi import IPLimiter, TotalLimiter
from throttled.models import Rate
from throttled.storage.memory import MemoryStorage

DEFAULT_RATE_LIMIT = 100
DEFAULT_RATE_LIMIT_WINDOW = 60

DEFAULT_TOTAL_RATE_LIMIT = 1000
DEFAULT_TOTAL_RATE_LIMIT_WINDOW = 60

RATE_LIMIT = int(os.environ.get("RATE_LIMIT", DEFAULT_RATE_LIMIT))
RATE_LIMIT_WINDOW = int(os.environ.get("RATE_LIMIT_WINDOW", DEFAULT_RATE_LIMIT_WINDOW))

TOTAL_RATE_LIMIT = int(os.environ.get("TOTAL_RATE_LIMIT", DEFAULT_TOTAL_RATE_LIMIT))
TOTAL_RATE_LIMIT_WINDOW = int(
    os.environ.get("TOTAL_RATE_LIMIT_WINDOW", DEFAULT_TOTAL_RATE_LIMIT_WINDOW)
)


def setup(app: FastAPI):
    storage = MemoryStorage(cache={})

    # global ceiling that protects the backend from aggregate overload
    total_limiter = TotalLimiter(
        limit=Rate(TOTAL_RATE_LIMIT, TOTAL_RATE_LIMIT_WINDOW), storage=storage
    )

    # per-client fairness limited by source ip using a sliding window
    ip_limiter = IPLimiter(limit=Rate(RATE_LIMIT, RATE_LIMIT_WINDOW), storage=storage)

    app.add_middleware(BaseHTTPMiddleware, dispatch=total_limiter.dispatch)
    app.add_middleware(BaseHTTPMiddleware, dispatch=ip_limiter.dispatch)
