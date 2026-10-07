from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.thingspeak_service import thingspeak_service
from app.services.ml_service import ml_service

router = APIRouter()

@router.get("/api/telemetry/latest")
def get_latest_telemetry():
    try:
        data = thingspeak_service.get_latest_data()
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error while fetching telemetry.")

@router.get("/api/predict/live")
def predict_live():
    # 1. Fetch telemetry
    try:
        data = thingspeak_service.get_latest_data()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error while fetching telemetry.")

    # 2. Extract timestamp to Day and Time_in_Hours
    # We assume UTC timestamp from ThingSpeak: e.g. "2026-04-01T00:30:00Z"
    ts_str = data["timestamp"]
    try:
        # handle the 'Z' suffix for python < 3.11
        if ts_str.endswith('Z'):
            ts_str = ts_str[:-1] + '+00:00'
        dt = datetime.fromisoformat(ts_str)
        # Assuming 'Day' in the original dataset meant day of the month or a sequential day
        day = dt.day
        # Time in hours
        time_in_hours = dt.hour + (dt.minute / 60.0) + (dt.second / 3600.0)
    except Exception as e:
        # Fallback if timestamp parsing fails
        raise HTTPException(status_code=400, detail=f"Failed to parse timestamp from ThingSpeak: {ts_str}")

    # 3. Predict using existing ML Service
    try:
        prediction = ml_service.predict(
            temperature=data["temperature"],
            humidity=data["humidity"],
            soil_moisture=data["soil_moisture"],
            light=data["light"],
            day=day,
            time_in_hours=time_in_hours
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
