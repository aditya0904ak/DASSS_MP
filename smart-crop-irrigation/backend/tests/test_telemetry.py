from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_telemetry_latest_success():
    mock_data = {
        "timestamp": "2024-05-13T12:00:00Z",
        "soil_moisture": 35.0,
        "temperature": 24.0,
        "humidity": 40.0,
        "light": 1000.0
    }
    with patch("app.routes.telemetry.thingspeak_service.get_latest_data", return_value=mock_data):
        response = client.get("/api/telemetry/latest")
        assert response.status_code == 200
        assert response.json() == mock_data

def test_telemetry_unavailable():
    with patch("app.routes.telemetry.thingspeak_service.get_latest_data", side_effect=ConnectionError("ThingSpeak down")):
        response = client.get("/api/telemetry/latest")
        assert response.status_code == 502
        assert "ThingSpeak down" in response.json()["detail"]

def test_telemetry_empty_response():
    with patch("app.routes.telemetry.thingspeak_service.get_latest_data", side_effect=ValueError("Empty response from ThingSpeak.")):
        response = client.get("/api/telemetry/latest")
        assert response.status_code == 400
        assert "Empty" in response.json()["detail"]

def test_telemetry_missing_field():
    with patch("app.routes.telemetry.thingspeak_service.get_latest_data", side_effect=ValueError("Missing sensor field in ThingSpeak response.")):
        response = client.get("/api/telemetry/latest")
        assert response.status_code == 400
        assert "Missing sensor field" in response.json()["detail"]

def test_telemetry_invalid_data():
    with patch("app.routes.telemetry.thingspeak_service.get_latest_data", side_effect=ValueError("Invalid sensor value")):
        response = client.get("/api/telemetry/latest")
        assert response.status_code == 400
        assert "Invalid sensor value" in response.json()["detail"]

def test_predict_live_success():
    mock_data = {
        "timestamp": "2024-05-13T12:00:00Z",
        "soil_moisture": 35.0,
        "temperature": 24.0,
        "humidity": 40.0,
        "light": 1000.0
    }
    mock_prediction = {
        "pump_prediction": 1,
        "irrigation_required": True,
        "confidence": 0.87
    }
    with patch("app.routes.telemetry.thingspeak_service.get_latest_data", return_value=mock_data):
        with patch("app.routes.telemetry.ml_service.predict", return_value=mock_prediction):
            response = client.get("/api/predict/live")
            assert response.status_code == 200
            json_resp = response.json()
            assert json_resp["timestamp"] == mock_data["timestamp"]
            assert json_resp["sensor_data"]["soil_moisture"] == mock_data["soil_moisture"]
            assert json_resp["sensor_data"]["temperature"] == mock_data["temperature"]
            assert json_resp["sensor_data"]["humidity"] == mock_data["humidity"]
            assert json_resp["sensor_data"]["light"] == mock_data["light"]
            assert json_resp["prediction"] == mock_prediction

def test_predict_live_ml_failure():
    mock_data = {
        "timestamp": "2024-05-13T12:00:00Z",
        "soil_moisture": 35.0,
        "temperature": 24.0,
        "humidity": 40.0,
        "light": 1000.0
    }
    with patch("app.routes.telemetry.thingspeak_service.get_latest_data", return_value=mock_data):
        with patch("app.routes.telemetry.ml_service.predict", side_effect=Exception("ML Error")):
            response = client.get("/api/predict/live")
            assert response.status_code == 500
            assert "Prediction failed" in response.json()["detail"]
