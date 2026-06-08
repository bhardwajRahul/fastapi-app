from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from helpers import cors


def test_no_cors(app: FastAPI, client: TestClient):
    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    response = client.get("/")
    assert "access-control-allow-origin" not in response.headers


def test_wildcard_origin_disables_credentials():
    app = FastAPI()

    with patch.object(cors, "ALLOWED_ORIGINS", "*"):
        cors.setup(app)

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    client = TestClient(app)

    response = client.get("/", headers={"Origin": "https://evil.example"})

    assert response.headers.get("access-control-allow-origin") == "*"
    assert "access-control-allow-credentials" not in response.headers


def test_explicit_origin_allows_credentials():
    app = FastAPI()

    with patch.object(cors, "ALLOWED_ORIGINS", "https://myhost.com"):
        cors.setup(app)

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    client = TestClient(app)

    allowed = client.get("/", headers={"Origin": "https://myhost.com"})
    assert allowed.headers.get("access-control-allow-origin") == "https://myhost.com"
    assert allowed.headers.get("access-control-allow-credentials") == "true"

    blocked = client.get("/", headers={"Origin": "https://evil.example"})
    assert "access-control-allow-origin" not in blocked.headers
