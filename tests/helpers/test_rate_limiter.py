from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from helpers import rate_limiter


def test_rate_limiter_allows_within_limit():
    app = FastAPI()

    with patch.object(rate_limiter, "RATE_LIMIT", 3):
        with patch.object(rate_limiter, "TOTAL_RATE_LIMIT", 100):
            rate_limiter.setup(app)

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    client = TestClient(app)

    codes = [client.get("/").status_code for _ in range(3)]
    assert codes == [200, 200, 200]


def test_rate_limiter_blocks_per_ip():
    app = FastAPI()

    with patch.object(rate_limiter, "RATE_LIMIT", 2):
        with patch.object(rate_limiter, "TOTAL_RATE_LIMIT", 100):
            rate_limiter.setup(app)

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    client = TestClient(app)

    allowed = [client.get("/").status_code for _ in range(2)]
    blocked = client.get("/")

    assert allowed == [200, 200]
    assert blocked.status_code == 429
    assert "retry-after" in blocked.headers


def test_rate_limiter_blocks_on_total_ceiling():
    app = FastAPI()

    with patch.object(rate_limiter, "RATE_LIMIT", 100):
        with patch.object(rate_limiter, "TOTAL_RATE_LIMIT", 2):
            rate_limiter.setup(app)

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    client = TestClient(app)

    allowed = [client.get("/").status_code for _ in range(2)]
    blocked = client.get("/")

    assert allowed == [200, 200]
    assert blocked.status_code == 429
    assert "retry-after" in blocked.headers
