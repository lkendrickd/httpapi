import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.service import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_create_app():
    app = create_app()
    assert isinstance(app, FastAPI)
    assert len(app.routes) == 3
    assert app.routes[0] == app.routes[1] == app.routes[2]
    assert app.routes[0] == app.routes[2]


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

# Add more tests as needed
