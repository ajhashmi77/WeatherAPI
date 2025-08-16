import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from app.main import app
import json

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_redis():
    with patch('app.main.redis_client') as mock:
        mock.get = MagicMock()
        mock.setex = MagicMock()
        yield mock

@pytest.fixture
def mock_httpx():
    with patch('app.main.httpx.AsyncClient') as mock:
        async_client = AsyncMock()
        mock.return_value.__aenter__.return_value = async_client
        yield async_client

def test_get_weather_success(client, mock_redis, mock_httpx):
    # Setup mocks
    mock_redis.get.return_value = None
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"weather": "clear"}
    mock_httpx.get.return_value = mock_response

    response = client.get("/weather?city=London")
    
    assert response.status_code == 200
    assert response.json()["source"] == "API"
    mock_redis.setex.assert_called_once()

def test_get_weather_cached(client, mock_redis):
    mock_redis.get.return_value = json.dumps({"weather": "clear"})
    
    response = client.get("/weather?city=London")
    
    assert response.status_code == 200
    assert response.json()["source"] == "cache"

def test_get_weather_api_failure(client, mock_redis, mock_httpx):
    mock_redis.get.return_value = None
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.json.return_value = {"message": "Invalid API key"}
    mock_httpx.get.return_value = mock_response

    response = client.get("/weather?city=London")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"