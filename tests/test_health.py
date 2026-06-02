from __future__ import annotations

from collections.abc import Iterator

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app


def test_liveness(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_db_up(client: TestClient) -> None:
    response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}


def test_health_db_down(client: TestClient) -> None:
    class _FailingSession:
        def execute(self, *args: object, **kwargs: object) -> None:
            raise RuntimeError("banco fora do ar")

    def _broken_db() -> Iterator[_FailingSession]:
        yield _FailingSession()

    app.dependency_overrides[get_db] = _broken_db
    try:
        response = client.get("/health/db")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert "indispon" in response.json()["detail"].lower()


def test_cors_preflight_allowed(client: TestClient) -> None:
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    assert response.headers.get("access-control-allow-credentials") == "true"


def test_cors_origin_not_allowed(client: TestClient) -> None:
    response = client.get("/health", headers={"Origin": "http://evil.com"})
    assert "access-control-allow-origin" not in response.headers
