from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    temperature: float = Field(..., ge=-50.0, le=100.0, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0.0, le=100.0, description="Humidity percentage")
    soil_moisture: float = Field(..., ge=0.0, le=100.0, description="Soil Moisture percentage")
    light: float = Field(..., ge=0.0, description="Light Intensity")
    day: int = Field(..., ge=1, description="Day (e.g., day of month or year)")
    time_in_hours: float = Field(..., ge=0.0, lt=24.0, description="Time in hours (0.0 to 23.99)")

class PredictionResponse(BaseModel):
    pump_prediction: int
    irrigation_required: bool
    confidence: float
