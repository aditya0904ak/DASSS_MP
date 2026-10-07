import os
import joblib
import pandas as pd

class MLService:
    def __init__(self):
        # We assume backend is running from smart-crop-irrigation/backend
        # Model path is ../ml/models
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.models_dir = os.path.join(base_dir, '..', 'ml', 'models')
        
        # We will load these lazily or on startup
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.requires_scaling = False
        
    def load_model(self):
        model_path = os.path.join(self.models_dir, 'irrigation_model.pkl')
        scaler_path = os.path.join(self.models_dir, 'scaler.pkl')
        features_path = os.path.join(self.models_dir, 'feature_names.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model file not found. Please train the model first.")
            
        model_data = joblib.load(model_path)
        self.model = model_data['model']
        self.requires_scaling = model_data.get('requires_scaling', False)
        
        if self.requires_scaling and os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path)
            
        if os.path.exists(features_path):
            self.feature_names = joblib.load(features_path)
            
    def predict(self, temperature, humidity, soil_moisture, light, day, time_in_hours):
        if self.model is None:
            self.load_model()
            
        # Reconstruct hour and minute
        hour = int(time_in_hours)
        minute = int(round((time_in_hours - hour) * 60.0))
        
        # Map to expected feature names
        input_data = {
            'Day': day,
            'Temperature_C': temperature,
            'Humidity_pct': humidity,
            'Soil_Moisture_pct': soil_moisture,
            'Light_Intensity': light,
            'hour': hour,
            'minute': minute,
            'time_in_hours': time_in_hours
        }
        
        df = pd.DataFrame([input_data])
        
        # Ensure correct column order if feature_names exists
        if self.feature_names:
            for col in self.feature_names:
                if col not in df.columns:
                    df[col] = 0
            df = df[self.feature_names]
            
        X = df
        if self.requires_scaling and self.scaler:
            X = self.scaler.transform(df)
            
        prediction = int(self.model.predict(X)[0])
        
        confidence = 1.0 # default if no proba
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(X)[0]
            confidence = float(proba[1]) if prediction == 1 else float(proba[0])
            
        return {
            "pump_prediction": prediction,
            "irrigation_required": bool(prediction),
            "confidence": confidence
        }

ml_service = MLService()
