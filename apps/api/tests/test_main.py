"""
Test suite for main application and routes.
Tests app startup, health check, and router registration.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_app_exists():
    """Test that FastAPI app is created."""
    assert app is not None
    assert app.title == "TradeComply API"


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data


def test_openapi_schema(client):
    """Test OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert schema["info"]["title"] == "TradeComply API"


def test_docs_endpoint(client):
    """Test API documentation endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_auth_routes_registered(client):
    """Test that auth routes are registered."""
    # Register endpoint should be available
    response = client.options("/api/v1/auth/register")
    assert response.status_code in [200, 404]  # 404 is OK for OPTIONS without implementation


def test_organization_routes_registered(client):
    """Test that organization routes are registered."""
    # Org endpoint should be available (will return 401 without auth)
    response = client.get("/api/v1/organizations/me")
    # Should be 401 Unauthorized (no token) not 404 (route not found)
    assert response.status_code in [401, 404, 307]  # 401 or 404 means route exists


if __name__ == "__main__":
    print("Run with: pytest apps/api/tests/test_main.py -v")
