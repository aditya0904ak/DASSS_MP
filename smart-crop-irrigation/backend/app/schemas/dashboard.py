from typing import Optional
from pydantic import BaseModel, Field

class SensorData(BaseModel):
    soil_moisture: float = Field(..., description="Soil moisture percentage")
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Humidity percentage")
    light: float = Field(..., description="LDR raw reading (ADC count)")

class PredictionData(BaseModel):
    pump_prediction: int = Field(..., description="Predicted pump status: 0 for OFF, 1 for ON")
    irrigation_required: bool = Field(..., description="Model prediction interpretation: True if irrigation recommended, False otherwise")
    confidence: Optional[float] = Field(None, description="Model prediction probability confidence, or null if unsupported")
    low_moisture_warning: bool = Field(False, description="Agronomic low-moisture alert: True if real Soil Moisture < 40%")
    moisture_threshold: float = Field(40.0, description="Configured low-moisture threshold percentage")

class IrrigationDecision(BaseModel):
    status: str = Field(..., description="IRRIGATION REQUIRED, IRRIGATION NOT REQUIRED, or WAITING FOR VALID SENSOR DATA")
    irrigation_required: Optional[bool] = Field(None, description="True if required, False if not required, None if waiting for data")
    reason: str = Field(..., description="Short dynamic reason for the decision")
    threshold: float = Field(default=40.0, description="Configured soil moisture threshold percentage")

class SystemStatus(BaseModel):
    status: str = Field(..., description="Telemetry freshness status: 'LIVE' or 'STALE'")
    data_source: str = Field(default="ThingSpeak", description="Origin of telemetry data")
    model_loaded: bool = Field(default=True, description="Whether the ML model is currently loaded in memory")

class DashboardResponse(BaseModel):
    timestamp: str = Field(..., description="Actual ThingSpeak feed creation timestamp")
    sensor_data: SensorData
    irrigation_decision: IrrigationDecision
    prediction: Optional[PredictionData] = None
    system: SystemStatus
