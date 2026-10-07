from fastapi import APIRouter, HTTPException
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.ml_service import ml_service

router = APIRouter()

@router.post("/api/predict", response_model=PredictionResponse)
def predict_irrigation(request: PredictionRequest):
    try:
        result = ml_service.predict(
            temperature=request.temperature,
            humidity=request.humidity,
            soil_moisture=request.soil_moisture,
            light=request.light,
            day=request.day,
            time_in_hours=request.time_in_hours
        )
        return PredictionResponse(
            pump_prediction=result["pump_prediction"],
            irrigation_required=result["irrigation_required"],
            confidence=result["confidence"]
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        # Log this internally in a real app
        print(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed due to internal error.")
