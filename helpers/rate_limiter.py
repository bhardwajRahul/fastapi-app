import os

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from throttled.fastapi import IPLimiter
from throttled.models import Rate
from throttled.storage.memory import MemoryStorage

DEFAULT_RATE_LIMIT = 100
DEFAULT_RATE_LIMIT_WINDOW = 60

RATE_LIMIT = int(os.environ.get("RATE_LIMIT", DEFAULT_RATE_LIMIT))
RATE_LIMIT_WINDOW = int(os.environ.get("RATE_LIMIT_WINDOW", DEFAULT_RATE_LIMIT_WINDOW))


def setup(app: FastAPI):
    storage = MemoryStorage(cache={})

    # limit each client by its source ip using a sliding window
    limiter = IPLimiter(limit=Rate(RATE_LIMIT, RATE_LIMIT_WINDOW), storage=storage)

    app.add_middleware(BaseHTTPMiddleware, dispatch=limiter.dispatch)
