import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.services.ml_service import MLService, ml_service
from app.services.thingspeak_service import thingspeak_service
from app.utils.time_utils import parse_thingspeak_timestamp, calculate_freshness

client = TestClient(app)

class MockEstimatorWithProba:
    def __init__(self, classes, proba_return, pred_return):
        self.classes_ = classes
        self._proba_return = proba_return
        self._pred_return = pred_return

    def predict(self, X):
        return [self._pred_return]

    def predict_proba(self, X):
        return [self._proba_return]

class MockEstimatorNoProba:
    def __init__(self, pred_return):
        self._pred_return = pred_return

    def predict(self, X):
        return [self._pred_return]

def test_dashboard_success_live():
    # Construct a fresh UTC timestamp (5 seconds ago)
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mock_telemetry = {
        "timestamp": now_utc,
        "soil_moisture": 45.0,
        "temperature": 28.5,
        "humidity": 65.0,
        "light": 1250.0
    }
    mock_prediction = {
        "pump_prediction": 1,
        "irrigation_required": True,
        "confidence": 0.9421
    }

    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        with patch.object(ml_service, "predict", return_value=mock_prediction):
            response = client.get("/api/dashboard")
            assert response.status_code == 200
            data = response.json()
            
            assert data["timestamp"] == now_utc
            assert data["sensor_data"]["soil_moisture"] == 45.0
            assert data["sensor_data"]["temperature"] == 28.5
            assert data["sensor_data"]["humidity"] == 65.0
            assert data["sensor_data"]["light"] == 1250.0
            
            assert data["prediction"]["pump_prediction"] == 1
            assert data["prediction"]["irrigation_required"] is True
            assert data["prediction"]["confidence"] == 0.9421
            
            assert data["system"]["status"] == "LIVE"
            assert data["system"]["data_source"] == "ThingSpeak"
            assert data["system"]["model_loaded"] is True

def test_dashboard_sensor_field_mapping():
    """Verify that all four ThingSpeak fields map exactly to sensor parameters."""
    feed = {
        "created_at": "2026-10-12T10:00:00Z",
        "entry_id": 100,
        "field1": "33.2",
        "field2": "27.4",
        "field3": "55.8",
        "field4": "850"
    }
    with patch.object(thingspeak_service, "_fetch_data", return_value=[feed]):
        response = client.get("/api/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert data["sensor_data"]["soil_moisture"] == 33.2
        assert data["sensor_data"]["temperature"] == 27.4
        assert data["sensor_data"]["humidity"] == 55.8
        assert data["sensor_data"]["light"] == 850.0

def test_dashboard_time_feature_derivation():
    """Test timestamp parsing and Day / Time_in_Hours derivation in IST timezone."""
    # 2026-10-12T06:30:00Z in UTC is 2026-10-12 12:00:00 in Asia/Kolkata (+05:30)
    meta = parse_thingspeak_timestamp("2026-10-12T06:30:00Z")
    assert meta["day"] == 12
    assert meta["hour"] == 12
    assert meta["minute"] == 0
    assert meta["time_in_hours"] == 12.0

def test_dashboard_stale_telemetry():
    """Verify that feeds older than freshness threshold are marked STALE."""
    old_timestamp = "2026-10-06T13:59:24Z"
    mock_telemetry = {
        "timestamp": old_timestamp,
        "soil_moisture": 30.0,
        "temperature": 25.0,
        "humidity": 50.0,
        "light": 500.0
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        response = client.get("/api/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert data["system"]["status"] == "STALE"

def test_dashboard_thingspeak_timeout():
    """Verify that ThingSpeak timeout raises 502 Bad Gateway."""
    with patch.object(thingspeak_service, "get_latest_data", side_effect=ConnectionError("Request timed out")):
        response = client.get("/api/dashboard")
        assert response.status_code == 502
        assert "timed out" in response.json()["detail"].lower()

def test_dashboard_thingspeak_http_error():
    """Verify that ThingSpeak invalid/missing channel raises 400 Bad Request."""
    with patch.object(thingspeak_service, "get_latest_data", side_effect=ValueError("ThingSpeak channel not found")):
        response = client.get("/api/dashboard")
        assert response.status_code == 400
        assert "not found" in response.json()["detail"].lower()

def test_dashboard_malformed_sensor_data():
    """Verify that malformed/missing sensor fields raise 400."""
    with patch.object(thingspeak_service, "get_latest_data", side_effect=ValueError("Invalid or missing sensor data")):
        response = client.get("/api/dashboard")
        assert response.status_code == 400
        assert "missing sensor data" in response.json()["detail"].lower()

def test_dashboard_model_not_found():
    """Verify that missing model file raises 503 Service Unavailable."""
    with patch.object(ml_service, "load_model", side_effect=FileNotFoundError("Model file not found")):
        with patch.object(ml_service, "model", None):
            response = client.get("/api/dashboard")
            assert response.status_code == 503
            assert "model file not found" in response.json()["detail"].lower()

def test_dashboard_prediction_failure():
    """Verify that prediction internal errors raise 500."""
    mock_telemetry = {
        "timestamp": "2026-10-12T10:00:00Z",
        "soil_moisture": 30.0,
        "temperature": 25.0,
        "humidity": 50.0,
        "light": 500.0
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        with patch.object(ml_service, "predict", side_effect=Exception("Dimension mismatch")):
            response = client.get("/api/dashboard")
            assert response.status_code == 500
            assert "prediction failed" in response.json()["detail"].lower()

def test_ml_confidence_extraction_with_classes_order():
    """Test that confidence correctly looks up the predicted class index in model.classes_."""
    service = MLService()
    # Reverse classes order [1, 0] to test that positive class is NOT blindly assumed at index 1
    service.model = MockEstimatorWithProba(classes=[1, 0], proba_return=[0.85, 0.15], pred_return=1)
    service.requires_scaling = False
    service.feature_names = ['Day', 'Temperature_C', 'Humidity_pct', 'Soil_Moisture_pct', 'Light_Intensity', 'hour', 'minute', 'time_in_hours']
    
    result = service.predict(temperature=25.0, humidity=50.0, soil_moisture=30.0, light=500.0, day=12, time_in_hours=14.0)
    assert result["pump_prediction"] == 1
    assert result["irrigation_required"] is True
    assert result["confidence"] == 0.85

    # Test class 0 prediction when class 0 is at index 1 in classes_
    service.model = MockEstimatorWithProba(classes=[1, 0], proba_return=[0.20, 0.80], pred_return=0)
    result = service.predict(temperature=25.0, humidity=50.0, soil_moisture=30.0, light=500.0, day=12, time_in_hours=14.0)
    assert result["pump_prediction"] == 0
    assert result["irrigation_required"] is False
    assert result["confidence"] == 0.80

def test_ml_confidence_none_when_no_predict_proba():
    """Verify that models without predict_proba return confidence: None without inventing values."""
    service = MLService()
    service.model = MockEstimatorNoProba(pred_return=0)
    service.requires_scaling = False
    service.feature_names = ['Day', 'Temperature_C', 'Humidity_pct', 'Soil_Moisture_pct', 'Light_Intensity', 'hour', 'minute', 'time_in_hours']
    
    result = service.predict(temperature=25.0, humidity=50.0, soil_moisture=30.0, light=500.0, day=12, time_in_hours=14.0)
    assert result["pump_prediction"] == 0
    assert result["irrigation_required"] is False
    assert result["confidence"] is None

def test_dashboard_low_moisture_warning_below_40():
    """Verify that soil moisture < 40% triggers low_moisture_warning."""
    mock_telemetry = {
        "timestamp": "2026-10-12T10:00:00Z",
        "soil_moisture": 7.0, # Critically dry (7%)
        "temperature": 32.0,
        "humidity": 40.0,
        "light": 1000.0
    }
    mock_prediction = {
        "pump_prediction": 0,
        "irrigation_required": False,
        "confidence": 1.0
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        with patch.object(ml_service, "predict", return_value=mock_prediction):
            response = client.get("/api/dashboard")
            assert response.status_code == 200
            data = response.json()
            assert data["prediction"]["low_moisture_warning"] is True
            assert data["sensor_data"]["soil_moisture"] == 7.0

def test_dashboard_low_moisture_warning_above_40():
    """Verify that soil moisture >= 40% has low_moisture_warning as False."""
    mock_telemetry = {
        "timestamp": "2026-10-12T10:00:00Z",
        "soil_moisture": 48.0,
        "temperature": 26.0,
        "humidity": 55.0,
        "light": 800.0
    }
    mock_prediction = {
        "pump_prediction": 0,
        "irrigation_required": False,
        "confidence": 1.0
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        with patch.object(ml_service, "predict", return_value=mock_prediction):
            response = client.get("/api/dashboard")
            assert response.status_code == 200
            data = response.json()
            assert data["prediction"]["low_moisture_warning"] is False

def test_ml_feature_ordering_and_missing_inputs():
    """Verify that input features are passed in exact expected order."""
    service = MLService()
    captured_cols = []
    class MockInspector:
        classes_ = [0, 1]
        def predict(self, X):
            nonlocal captured_cols
            captured_cols = list(X.columns)
            return [0]
        def predict_proba(self, X):
            return [[0.73, 0.27]]

    service.model = MockInspector()
    service.requires_scaling = False
    service.feature_names = ['Day', 'Temperature_C', 'Humidity_pct', 'Soil_Moisture_pct', 'Light_Intensity', 'hour', 'minute', 'time_in_hours']
    
    res = service.predict(temperature=28.0, humidity=45.0, soil_moisture=22.0, light=900.0, day=5, time_in_hours=16.5)
    assert captured_cols == ['Day', 'Temperature_C', 'Humidity_pct', 'Soil_Moisture_pct', 'Light_Intensity', 'hour', 'minute', 'time_in_hours']
    assert res["confidence"] == 0.73 # Real probability, not hardcoded 1.0

def test_dashboard_warning_disagreement_case():
    """
    Test the critical case: Soil Moisture is 18.0% (<40% threshold),
    but the ML model recommends Pump OFF (0) due to time-of-day bias.
    Verify that low_moisture_warning is True while pump_prediction is 0.
    """
    mock_telemetry = {
        "timestamp": "2026-10-12T14:00:00Z",
        "soil_moisture": 18.0,
        "temperature": 39.2,
        "humidity": 72.5,
        "light": 1001.0
    }
    mock_prediction = {
        "pump_prediction": 0,
        "irrigation_required": False,
        "confidence": 1.0
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        with patch.object(ml_service, "predict", return_value=mock_prediction):
            response = client.get("/api/dashboard")
            assert response.status_code == 200
            data = response.json()
            # Disagreement verified: safety warning active despite ML advising OFF
            assert data["sensor_data"]["soil_moisture"] == 18.0
            assert data["prediction"]["low_moisture_warning"] is True
            assert data["prediction"]["pump_prediction"] == 0
            assert data["prediction"]["irrigation_required"] is False

def test_dashboard_telemetry_snapshot_timestamp_consistency():
    """
    Verify that sensor cards and ML feature inputs use the exact same telemetry snapshot
    and timestamp, without substituting the system time.
    """
    feed_timestamp = "2026-10-12T08:30:15Z"
    mock_telemetry = {
        "timestamp": feed_timestamp,
        "soil_moisture": 38.0,
        "temperature": 30.0,
        "humidity": 60.0,
        "light": 1100.0
    }
    captured_predict_args = {}
    def mock_predict(**kwargs):
        nonlocal captured_predict_args
        captured_predict_args = kwargs
        return {"pump_prediction": 1, "irrigation_required": True, "confidence": 0.88}

    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        with patch.object(ml_service, "predict", side_effect=mock_predict):
            response = client.get("/api/dashboard")
            assert response.status_code == 200
            data = response.json()
            # Verify exact snapshot consistency
            assert data["timestamp"] == feed_timestamp
            assert data["sensor_data"]["soil_moisture"] == captured_predict_args["soil_moisture"] == 38.0
            assert data["sensor_data"]["temperature"] == captured_predict_args["temperature"] == 30.0
            assert data["sensor_data"]["humidity"] == captured_predict_args["humidity"] == 60.0
            assert data["sensor_data"]["light"] == captured_predict_args["light"] == 1100.0

def test_dashboard_moisture_60_model_off():
    """Case 2: Moisture 60%, model OFF -> no low-moisture warning."""
    mock_telemetry = {
        "timestamp": "2026-10-12T14:00:00Z",
        "soil_moisture": 60.0,
        "temperature": 25.0,
        "humidity": 55.0,
        "light": 700.0
    }
    mock_prediction = {
        "pump_prediction": 0,
        "irrigation_required": False,
        "confidence": 0.95
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        with patch.object(ml_service, "predict", return_value=mock_prediction):
            response = client.get("/api/dashboard")
            assert response.status_code == 200
            data = response.json()
            assert data["prediction"]["low_moisture_warning"] is False
            assert data["prediction"]["pump_prediction"] == 0
            assert data["prediction"]["moisture_threshold"] == 40.0

def test_dashboard_moisture_18_model_on():
    """Case 3: Moisture 18%, model ON -> warning visible and model prediction remains ON."""
    mock_telemetry = {
        "timestamp": "2026-10-12T06:00:00Z",
        "soil_moisture": 18.0,
        "temperature": 24.0,
        "humidity": 70.0,
        "light": 300.0
    }
    mock_prediction = {
        "pump_prediction": 1,
        "irrigation_required": True,
        "confidence": 0.88
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        with patch.object(ml_service, "predict", return_value=mock_prediction):
            response = client.get("/api/dashboard")
            assert response.status_code == 200
            data = response.json()
            assert data["prediction"]["low_moisture_warning"] is True
            assert data["prediction"]["pump_prediction"] == 1
            assert data["prediction"]["irrigation_required"] is True
            assert data["sensor_data"]["soil_moisture"] == 18.0

def test_rule_decision_moisture_18():
    """Case 1: Moisture 18% -> IRRIGATION REQUIRED."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mock_telemetry = {
        "timestamp": now_utc,
        "soil_moisture": 18.0,
        "temperature": 28.0,
        "humidity": 60.0,
        "light": 1000.0
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        response = client.get("/api/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert data["irrigation_decision"]["status"] == "IRRIGATION REQUIRED"
        assert data["irrigation_decision"]["irrigation_required"] is True
        assert "below the 40% threshold" in data["irrigation_decision"]["reason"]

def test_rule_decision_moisture_39():
    """Case 2: Moisture 39% -> IRRIGATION REQUIRED."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mock_telemetry = {
        "timestamp": now_utc,
        "soil_moisture": 39.0,
        "temperature": 26.0,
        "humidity": 55.0,
        "light": 800.0
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        response = client.get("/api/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert data["irrigation_decision"]["status"] == "IRRIGATION REQUIRED"
        assert data["irrigation_decision"]["irrigation_required"] is True
        assert "below the 40% threshold" in data["irrigation_decision"]["reason"]

def test_rule_decision_moisture_40():
    """Case 3: Moisture 40% -> IRRIGATION NOT REQUIRED."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mock_telemetry = {
        "timestamp": now_utc,
        "soil_moisture": 40.0,
        "temperature": 25.0,
        "humidity": 50.0,
        "light": 900.0
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        response = client.get("/api/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert data["irrigation_decision"]["status"] == "IRRIGATION NOT REQUIRED"
        assert data["irrigation_decision"]["irrigation_required"] is False
        assert "meeting the configured 40% threshold" in data["irrigation_decision"]["reason"]

def test_rule_decision_moisture_65():
    """Case 4: Moisture 65% -> IRRIGATION NOT REQUIRED."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mock_telemetry = {
        "timestamp": now_utc,
        "soil_moisture": 65.0,
        "temperature": 23.0,
        "humidity": 65.0,
        "light": 600.0
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        response = client.get("/api/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert data["irrigation_decision"]["status"] == "IRRIGATION NOT REQUIRED"
        assert data["irrigation_decision"]["irrigation_required"] is False
        assert "meeting the configured 40% threshold" in data["irrigation_decision"]["reason"]

def test_rule_decision_stale_or_invalid_moisture():
    """Case 5: Stale moisture -> WAITING FOR VALID SENSOR DATA."""
    stale_timestamp = "2026-10-06T12:00:00Z" # Old timestamp -> STALE
    mock_telemetry = {
        "timestamp": stale_timestamp,
        "soil_moisture": 18.0,
        "temperature": 28.0,
        "humidity": 60.0,
        "light": 1000.0
    }
    with patch.object(thingspeak_service, "get_latest_data", return_value=mock_telemetry):
        response = client.get("/api/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert data["system"]["status"] == "STALE"
        assert data["irrigation_decision"]["status"] == "WAITING FOR VALID SENSOR DATA"
        assert data["irrigation_decision"]["irrigation_required"] is None
        assert "stale" in data["irrigation_decision"]["reason"].lower()




