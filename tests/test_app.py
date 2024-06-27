import pytest
from fastapi.testclient import TestClient

from service.app import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_create_app():
    app = create_app()
    assert isinstance(app, FastAPI)
    assert any(route.path == "/metrics" for route in app.routes)
    assert any(route.path == "/health" for route in app.routes)
    assert any(route.path == "/" for route in app.routes)


def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    # Add more specific assertions based on what get_metrics returns


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    # Add more specific assertions based on what health_check returns


def test_index_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    # Add more specific assertions based on what get_index returns


def test_middleware_applied(client):
    # This test checks if the middleware is applied
    # You might need to adjust this based on what your middleware does
    response = client.get("/")
    assert response.status_code == 200
    # Add assertions to check if the middleware has been applied correctly


def test_error_handlers(client):
    # This test checks if error handlers are set up
    # You might need to trigger a specific error to test this
    response = client.get("/non-existent-path")
    assert response.status_code == 404
    # Add more assertions based on how your error handlers work
