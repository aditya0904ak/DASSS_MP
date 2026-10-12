import math
from fastapi import APIRouter, HTTPException
from app.schemas.dashboard import (
    DashboardResponse, 
    SensorData, 
    PredictionData, 
    SystemStatus, 
    IrrigationDecision
)
from app.services.thingspeak_service import thingspeak_service
from app.services.ml_service import ml_service
from app.utils.time_utils import parse_thingspeak_timestamp, calculate_freshness

router = APIRouter()

@router.get("/api/dashboard", response_model=DashboardResponse)
def get_dashboard_summary():
    """
    Unified dashboard endpoint that retrieves the latest actual ThingSpeak telemetry,
    derives dataset-aligned time features in the intended timezone, runs rule-based
    irrigation decision logic (primary decision maker), runs ML inference (retained for
    inspection), assesses data freshness, and returns consolidated telemetry and status.
    
    Rule-based Irrigation Decision:
    - IRRIGATION REQUIRED: Soil moisture < 40%
    - IRRIGATION NOT REQUIRED: Soil moisture >= 40%
    - WAITING FOR VALID SENSOR DATA: Soil moisture is missing, invalid, or stale
    """
    # 1. Ensure ML Model is loaded
    try:
        if ml_service.model is None:
            ml_service.load_model()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize ML model: {e}")

    # 2. Fetch latest telemetry (single request)
    try:
        data = thingspeak_service.get_latest_data()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch telemetry: {e}")

    # 3. Parse timestamp and derive feature inputs
    try:
        time_meta = parse_thingspeak_timestamp(data["timestamp"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process timestamp '{data.get('timestamp')}': {e}")

    # 4. Predict using existing ML service (retained for background experimentation)
    try:
        prediction = ml_service.predict(
            temperature=data["temperature"],
            humidity=data["humidity"],
            soil_moisture=data["soil_moisture"],
            light=data["light"],
            day=time_meta["day"],
            time_in_hours=time_meta["time_in_hours"]
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {e}")

    # 5. Calculate data freshness
    freshness = calculate_freshness(time_meta["utc_datetime"])
    is_stale = (freshness == "STALE")

    # 6. Rule-Based Irrigation Decision (Primary Decision Maker)
    threshold = 40.0
    moisture = data.get("soil_moisture")
    has_valid_moisture = (
        moisture is not None and 
        isinstance(moisture, (int, float)) and 
        math.isfinite(moisture)
    )

    if is_stale or not has_valid_moisture:
        decision_status = "WAITING FOR VALID SENSOR DATA"
        decision_required = None
        if is_stale:
            decision_reason = "Telemetry is stale (>120s old). Waiting for fresh sensor feed from Wokwi ESP32."
        else:
            decision_reason = "Soil moisture sensor reading is missing or invalid."
    elif moisture < threshold:
        decision_status = "IRRIGATION REQUIRED"
        decision_required = True
        decision_reason = f"Soil moisture is {moisture:g}%, below the {int(threshold)}% threshold."
    else:
        decision_status = "IRRIGATION NOT REQUIRED"
        decision_required = False
        decision_reason = f"Soil moisture is {moisture:g}%, meeting the configured {int(threshold)}% threshold."

    irrigation_decision = IrrigationDecision(
        status=decision_status,
        irrigation_required=decision_required,
        reason=decision_reason,
        threshold=threshold
    )

    return DashboardResponse(
        timestamp=data["timestamp"],
        sensor_data=SensorData(
            soil_moisture=data["soil_moisture"],
            temperature=data["temperature"],
            humidity=data["humidity"],
            light=data["light"]
        ),
        irrigation_decision=irrigation_decision,
        prediction=PredictionData(
            pump_prediction=prediction["pump_prediction"],
            irrigation_required=prediction["irrigation_required"],
            confidence=prediction["confidence"],
            low_moisture_warning=bool(has_valid_moisture and moisture < threshold),
            moisture_threshold=threshold
        ),
        system=SystemStatus(
            status=freshness,
            data_source="ThingSpeak",
            model_loaded=ml_service.model is not None
        )
    )
