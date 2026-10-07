import os
import joblib
import pandas as pd
from feature_engineering import create_features

def predict_irrigation(input_data):
    """
    input_data should be a dictionary like:
    {
        "Temperature_C": 25.5,
        "Humidity_pct": 45,
        "Soil_Moisture_pct": 30,
        "Light_Intensity": 800,
        "Day": 1,
        "Time": "14:30:00"
    }
    """
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    
    # Load assets
    model_data = joblib.load(os.path.join(models_dir, 'irrigation_model.pkl'))
    scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
    feature_names = joblib.load(os.path.join(models_dir, 'feature_names.pkl'))
    
    model = model_data['model']
    requires_scaling = model_data['requires_scaling']
    
    # Create a DataFrame from single input
    df = pd.DataFrame([input_data])
    
    # Apply the exact same feature engineering
    df = create_features(df)
    
    # Ensure all required features are present and in the right order
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0 # Default value if missing
            
    df = df[feature_names]
    
    # Scale if necessary
    X = df
    if requires_scaling:
        X = scaler.transform(df)
        
    # Predict
    prediction = int(model.predict(X)[0])
    
    # Try to get probability
    confidence = None
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(X)[0]
        confidence = float(proba[1]) if prediction == 1 else float(proba[0])
        
    result = {
        "pump_prediction": prediction,
        "irrigation_required": bool(prediction),
        "confidence": confidence
    }
    
    return result

if __name__ == '__main__':
    # Test script with a sample observation
    sample_input = {
        "Temperature_C": 30.0,
        "Humidity_pct": 40.0,
        "Soil_Moisture_pct": 25.0, # low soil moisture
        "Light_Intensity": 1000,
        "Day": 1,
        "Time": "12:00:00"
    }
    print("Testing with input:", sample_input)
    res = predict_irrigation(sample_input)
    print("Prediction Result:", res)