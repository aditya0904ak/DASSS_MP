# Smart Crop Irrigation Backend

This is the FastAPI backend serving the Machine Learning model predictions for the IoT-Based Smart Crop Water Management system.

## Setup & Installation

1. Make sure you are in the `backend` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables by copying `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   *Note: If ThingSpeak channel `3523427` is private, provide the `THINGSPEAK_READ_API_KEY` in `.env`. Otherwise, it can be left blank.*

## Starting the Server

Run the following command to start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The server will be available at `http://localhost:8000`.

## API Documentation

FastAPI automatically generates interactive Swagger documentation.
You can view it by going to:
[http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints

### 1. Health Check
- **URL**: `/api/health`
- **Method**: `GET`
- **Response**:
  ```json
  {
      "status": "ok",
      "model_loaded": true
  }
  ```

### 2. Predict Irrigation Needs
- **URL**: `/api/predict`
- **Method**: `POST`
- **Description**: Predicts whether irrigation is required based on manually provided sensor data.
- **Request Body**:
  ```json
  {
      "temperature": 24.0,
      "humidity": 40.0,
      "soil_moisture": 32.0,
      "light": 1000,
      "day": 10,
      "time_in_hours": 14.5
  }
  ```

### 3. Fetch Latest ThingSpeak Telemetry
- **URL**: `/api/telemetry/latest`
- **Method**: `GET`
- **Description**: Fetches the latest live data from ThingSpeak channel `3523427`.
- **Response**:
  ```json
  {
      "timestamp": "2024-05-13T12:00:00Z",
      "soil_moisture": 35.0,
      "temperature": 24.0,
      "humidity": 40.0,
      "light": 1000.0
  }
  ```

### 4. Live Irrigation Prediction (End-to-End)
- **URL**: `/api/predict/live`
- **Method**: `GET`
- **Description**: Fetches the latest ThingSpeak data, formats the timestamp into ML features (Day, Time_in_hours using UTC), and runs it through the saved model to return a live prediction.
- **Response**:
  ```json
  {
      "timestamp": "2024-05-13T12:00:00Z",
      "sensor_data": {
          "soil_moisture": 35.0,
          "temperature": 24.0,
          "humidity": 40.0,
          "light": 1000.0
      },
      "prediction": {
          "pump_prediction": 1,
          "irrigation_required": true,
          "confidence": 0.87
      }
  }
  ```

## ThingSpeak Integration Details

The backend communicates with **ThingSpeak Channel ID: 3523427**.
The data mapping expected from Wokwi is:
- **Field 1**: Soil Moisture
- **Field 2**: Temperature
- **Field 3**: Humidity
- **Field 4**: Light

Data is fetched via HTTP requests to `api.thingspeak.com`. If the channel is unreachable, private without a key, or returns empty/invalid data, the API will return a standard `400` or `502` HTTP error to prevent corrupted ML predictions.

## Model Dependency

This backend relies on the ML models trained in the `ml/` directory.
It looks for the model file at `../ml/models/irrigation_model.pkl`.
If the model file is not found, the prediction endpoint will return a `503 Service Unavailable` error. You must run the ML training pipeline first.
