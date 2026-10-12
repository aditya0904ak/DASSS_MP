# Smart Crop Irrigation Backend API

FastAPI backend serving real-time IoT telemetry integration and Machine Learning irrigation predictions for the **IoT-Based Smart Crop Water Management and Predictive Irrigation** platform.

---

## 1. Environment Variables

Configure these settings in `backend/.env` (refer to `.env.example`):

| Variable | Default | Description |
|---|---|---|
| `THINGSPEAK_CHANNEL_ID` | `3523427` | ThingSpeak telemetry channel ID |
| `THINGSPEAK_READ_API_KEY` | *(None)* | Read API key for private channels |
| `APP_TIMEZONE` | `Asia/Kolkata` | Intended timezone for time feature extraction (UTC offset +05:30) |
| `TELEMETRY_FRESHNESS_THRESHOLD_SECONDS` | `120` | Maximum age in seconds before telemetry is flagged as `STALE` |

*Security Notice: Never commit `.env` or write API keys into source code.*

---

## 2. Installation & Startup

### Setup Environment
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

### Start Server
```bash
uvicorn app.main:app --reload
```
Server runs at `http://localhost:8000`.  
Interactive Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 3. Automated Testing

Run the full pytest suite (30 unit & integration tests):

```bash
pytest -v
```

All tests mock external ThingSpeak network calls and ML estimators, running entirely offline without depending on network availability.

---

## 4. API Endpoints

### 1. Unified Dashboard Summary
- **Endpoint**: `GET /api/dashboard`
- **Description**: Consolidates the latest ThingSpeak telemetry, feature engineering, ML prediction, and system health into a single unified payload.
- **Response (`200 OK`)**:
  ```json
  {
    "timestamp": "2026-10-12T16:57:11Z",
    "sensor_data": {
      "soil_moisture": 15.0,
      "temperature": 38.3,
      "humidity": 42.5,
      "light": 2857.0
    },
    "prediction": {
      "pump_prediction": 0,
      "irrigation_required": false,
      "confidence": 1.0
    },
    "system": {
      "status": "LIVE",
      "data_source": "ThingSpeak",
      "model_loaded": true
    }
  }
  ```
  *Note: `irrigation_required` represents the ML model's advisory prediction, not a confirmation of physical relay activation.*

---

### 2. Latest Telemetry
- **Endpoint**: `GET /api/telemetry/latest`
- **Description**: Returns the latest parsed four-sensor telemetry reading from ThingSpeak.
- **Response (`200 OK`)**:
  ```json
  {
    "timestamp": "2026-10-12T16:57:11Z",
    "soil_moisture": 15.0,
    "temperature": 38.3,
    "humidity": 42.5,
    "light": 2857.0
  }
  ```

---

### 3. Historical Telemetry
- **Endpoint**: `GET /api/telemetry/history`
- **Query Parameter**: `results` (optional integer, bounded between `1` and `8000`, default `100`).
- **Description**: Returns deduplicated historical feeds sorted strictly in ascending chronological order. Malformed or null readings are pruned.
- **Response (`200 OK`)**:
  ```json
  [
    {
      "timestamp": "2026-10-12T16:51:15Z",
      "soil_moisture": 72.0,
      "temperature": 20.3,
      "humidity": 56.0,
      "light": 2436.0
    },
    {
      "timestamp": "2026-10-12T16:57:11Z",
      "soil_moisture": 15.0,
      "temperature": 38.3,
      "humidity": 42.5,
      "light": 2857.0
    }
  ]
  ```

---

### 4. Live Prediction
- **Endpoint**: `GET /api/predict/live`
- **Description**: Fetches the latest telemetry, derives time features, and executes the ML model.
- **Response (`200 OK`)**:
  ```json
  {
    "timestamp": "2026-10-12T16:57:11Z",
    "sensor_data": {
      "soil_moisture": 15.0,
      "temperature": 38.3,
      "humidity": 42.5,
      "light": 2857.0
    },
    "prediction": {
      "pump_prediction": 0,
      "irrigation_required": false,
      "confidence": 1.0
    }
  }
  ```

---

### 5. Manual Prediction
- **Endpoint**: `POST /api/predict`
- **Request Body**:
  ```json
  {
    "temperature": 24.0,
    "humidity": 40.0,
    "soil_moisture": 32.0,
    "light": 1000.0,
    "day": 10,
    "time_in_hours": 14.5
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "pump_prediction": 0,
    "irrigation_required": false,
    "confidence": 1.0
  }
  ```

---

### 6. Health Check
- **Endpoint**: `GET /api/health`
- **Response (`200 OK`)**:
  ```json
  {
    "status": "ok",
    "model_loaded": true
  }
  ```

---

## 5. Timestamp & Feature Engineering

ThingSpeak stores feed timestamps in UTC ISO 8601 (e.g., `2026-10-12T16:57:11Z`).  
To match the original training dataset (`Edge_IoT_Predictive_Irrigation_Dataset.xlsx`), timestamps are processed as follows:

1. **Timezone Conversion**: Converted to `APP_TIMEZONE` (`Asia/Kolkata`, UTC+05:30), reflecting the agricultural diurnal cycle.
2. **Feature Extraction**:
   - `Day`: Day of the month extracted from the local timestamp (`dt_local.day`).
   - `hour`: Hour of the day (`0-23`).
   - `minute`: Minute of the hour (`0-59`).
   - `time_in_hours`: Floating-point hour representation (`hour + minute/60.0 + second/3600.0`).
3. **Exact Feature Order**: Features are ordered according to `ml/models/feature_names.pkl`:  
   `['Day', 'Temperature_C', 'Humidity_pct', 'Soil_Moisture_pct', 'Light_Intensity', 'hour', 'minute', 'time_in_hours']`.
4. **Confidence Extraction**:
   - Probabilities are extracted using `model.classes_` to match the exact index of the predicted class.
   - If the model lacks `predict_proba()`, `confidence` returns `null` without fabricating default values.

---

## 6. Telemetry Freshness Rules

- **Upload Interval**: Free-tier ThingSpeak channels accept telemetry every 15–20 seconds from the Wokwi ESP32.
- **Freshness Window**: Evaluated as `(now_utc - feed_timestamp_utc).total_seconds()`.
- **Status Codes**:
  - `LIVE`: Telemetry age $\le$ `TELEMETRY_FRESHNESS_THRESHOLD_SECONDS` (120s).
  - `STALE`: Telemetry age > 120s.

---

## 7. Error Handling

- **`400 Bad Request`**: Malformed timestamp, missing/non-numeric sensor fields, or empty ThingSpeak feed list.
- **`422 Unprocessable Entity`**: Validation failures on request parameters or body fields.
- **`502 Bad Gateway`**: ThingSpeak API connection timeout or external HTTP gateway failure.
- **`503 Service Unavailable`**: ML model artifact (`irrigation_model.pkl`) not found or failed to load.
- **`500 Internal Server Error`**: Unexpected internal inference error.
