import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_weather():
    response = client.get("/weather?city=London")
    assert response.status_code == 200
    assert "source" in response.json()