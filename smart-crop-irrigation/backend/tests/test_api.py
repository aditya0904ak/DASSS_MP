from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    # model_loaded might be true or false depending on the environment, 
    # but we just check the key exists.
    assert "model_loaded" in data

def test_valid_prediction():
    payload = {
        "temperature": 24.0,
        "humidity": 40.0,
        "soil_moisture": 32.0,
        "light": 1000,
        "day": 10,
        "time_in_hours": 14.5
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "pump_prediction" in data
    assert "irrigation_required" in data
    assert "confidence" in data
    assert data["pump_prediction"] in [0, 1]

def test_invalid_humidity():
    payload = {
        "temperature": 24.0,
        "humidity": 150.0, # invalid, > 100
        "soil_moisture": 32.0,
        "light": 1000,
        "day": 10,
        "time_in_hours": 14.5
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422 # Unprocessable Entity (validation error)

def test_invalid_soil_moisture():
    payload = {
        "temperature": 24.0,
        "humidity": 40.0,
        "soil_moisture": -10.0, # invalid, < 0
        "light": 1000,
        "day": 10,
        "time_in_hours": 14.5
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422

def test_missing_required_field():
    payload = {
        "temperature": 24.0,
        "humidity": 40.0,
        "light": 1000,
        "day": 10,
        "time_in_hours": 14.5
    }
    # missing soil_moisture
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422
