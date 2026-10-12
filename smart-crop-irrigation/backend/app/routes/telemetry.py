from fastapi import APIRouter, HTTPException, Query
from app.services.thingspeak_service import thingspeak_service
from app.services.ml_service import ml_service
from app.utils.time_utils import parse_thingspeak_timestamp

router = APIRouter()

@router.get("/api/telemetry/latest")
def get_latest_telemetry():
    """
    Fetch the latest valid telemetry readings from ThingSpeak channel.
    """
    try:
        data = thingspeak_service.get_latest_data()
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error while fetching telemetry.")

@router.get("/api/telemetry/history")
def get_telemetry_history(
    results: int = Query(default=100, ge=1, le=8000, description="Number of historical entries to fetch (bounded 1 to 8000)")
):
    """
    Fetch historical feeds from ThingSpeak, normalized, deduplicated by timestamp,
    and sorted chronologically.
    """
    try:
        data = thingspeak_service.get_history_data(results=results)
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error while fetching telemetry history.")

@router.get("/api/predict/live")
def predict_live():
    """
    End-to-end prediction endpoint: fetches latest telemetry from ThingSpeak,
    derives time features, and returns sensor data with ML prediction.
    """
    # 1. Fetch telemetry
    try:
        data = thingspeak_service.get_latest_data()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error while fetching telemetry.")

    # 2. Extract timestamp to Day and Time_in_Hours using centralized time utility
    try:
        time_meta = parse_thingspeak_timestamp(data["timestamp"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse timestamp from ThingSpeak: {data.get('timestamp')}")

    # 3. Predict using existing ML Service
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
        raise HTTPException(status_code=500, detail="Prediction failed due to internal error.")
        
    return {
        "timestamp": data["timestamp"],
        "sensor_data": {
            "soil_moisture": data["soil_moisture"],
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "light": data["light"]
        },
        "prediction": {
            "pump_prediction": prediction["pump_prediction"],
            "irrigation_required": prediction["irrigation_required"],
            "confidence": prediction["confidence"]
        }
    }
