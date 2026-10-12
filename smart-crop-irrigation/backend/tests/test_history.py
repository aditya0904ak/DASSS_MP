import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.thingspeak_service import thingspeak_service

client = TestClient(app)

def test_history_normalization_and_ordering():
    """Verify historical telemetry normalization and strict chronological ordering."""
    # Out of order feeds
    raw_feeds = [
        {
            "created_at": "2026-10-12T12:00:00Z",
            "entry_id": 2,
            "field1": "40.0",
            "field2": "26.5",
            "field3": "50.0",
            "field4": "900.0"
        },
        {
            "created_at": "2026-10-12T11:00:00Z",
            "entry_id": 1,
            "field1": "35.0",
            "field2": "25.0",
            "field3": "55.0",
            "field4": "800.0"
        }
    ]
    with patch.object(thingspeak_service, "_fetch_data", return_value=raw_feeds):
        response = client.get("/api/telemetry/history?results=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        # Earliest first
        assert data[0]["timestamp"] == "2026-10-12T11:00:00Z"
        assert data[0]["soil_moisture"] == 35.0
        assert data[0]["temperature"] == 25.0
        assert data[0]["humidity"] == 55.0
        assert data[0]["light"] == 800.0

        assert data[1]["timestamp"] == "2026-10-12T12:00:00Z"
        assert data[1]["soil_moisture"] == 40.0

def test_history_deduplication():
    """Verify duplicate timestamps are removed without repeating entries."""
    raw_feeds = [
        {
            "created_at": "2026-10-12T11:00:00Z",
            "entry_id": 1,
            "field1": "35.0",
            "field2": "25.0",
            "field3": "55.0",
            "field4": "800.0"
        },
        {
            "created_at": "2026-10-12T11:00:00Z",
            "entry_id": 2,
            "field1": "35.0",
            "field2": "25.0",
            "field3": "55.0",
            "field4": "800.0"
        }
    ]
    with patch.object(thingspeak_service, "_fetch_data", return_value=raw_feeds):
        response = client.get("/api/telemetry/history")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

def test_history_malformed_feeds_filtered():
    """Verify feeds with null or malformed fields are discarded without failing the whole request."""
    raw_feeds = [
        {
            "created_at": "2026-10-12T11:00:00Z",
            "entry_id": 1,
            "field1": "35.0",
            "field2": "25.0",
            "field3": "55.0",
            "field4": "800.0"
        },
        {
            "created_at": "2026-10-12T11:30:00Z",
            "entry_id": 2,
            "field1": None, # Null field
            "field2": "25.0",
            "field3": "55.0",
            "field4": "800.0"
        },
        {
            "created_at": "2026-10-12T12:00:00Z",
            "entry_id": 3,
            "field1": "45.0",
            "field2": "abc", # Invalid float
            "field3": "55.0",
            "field4": "800.0"
        }
    ]
    with patch.object(thingspeak_service, "_fetch_data", return_value=raw_feeds):
        response = client.get("/api/telemetry/history")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["timestamp"] == "2026-10-12T11:00:00Z"

def test_history_empty_response():
    """Verify empty feeds from ThingSpeak raise 400 error."""
    with patch.object(thingspeak_service, "_fetch_data", return_value=[]):
        response = client.get("/api/telemetry/history")
        assert response.status_code == 400
        assert "empty response" in response.json()["detail"].lower()

def test_history_invalid_bounds():
    """Verify results parameter validation bounds (ge=1, le=8000)."""
    response_low = client.get("/api/telemetry/history?results=0")
    assert response_low.status_code == 422 # FastAPI validation error

    response_high = client.get("/api/telemetry/history?results=99999")
    assert response_high.status_code == 422 # FastAPI validation error

def test_history_thingspeak_unavailable():
    """Verify ThingSpeak connection failure raises 502."""
    with patch.object(thingspeak_service, "_fetch_data", side_effect=ConnectionError("ThingSpeak connection timeout")):
        response = client.get("/api/telemetry/history")
        assert response.status_code == 502
        assert "timeout" in response.json()["detail"].lower()
