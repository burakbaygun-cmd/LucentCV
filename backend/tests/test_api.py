import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "gemini" in data

def test_get_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "2.0.0", "environment": "development"}

# To test other endpoints without triggering real Gemini API/Supabase calls,
# we would typically use unittest.mock.patch to mock get_ai_service and get_analysis_repo dependencies.
