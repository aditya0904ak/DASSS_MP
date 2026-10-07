from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.prediction import router as prediction_router
from app.routes.telemetry import router as telemetry_router
from app.services.ml_service import ml_service

app = FastAPI(title="Smart Crop Irrigation API")

# Setup CORS
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(prediction_router)
app.include_router(telemetry_router)

@app.get("/api/health")
def health_check():
    model_loaded = False
    try:
        if ml_service.model is None:
            ml_service.load_model()
        model_loaded = ml_service.model is not None
    except Exception as e:
        model_loaded = False
        print(f"Health check model load error: {e}")
        
    return {
        "status": "ok",
        "model_loaded": model_loaded
    }
