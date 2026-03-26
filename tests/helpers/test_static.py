from fastapi import FastAPI
from fastapi.testclient import TestClient

from helpers import static


def test_static_files():
    app = FastAPI()
    static.setup(app)
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "FastAPI App" in response.text
