import pandas as pd
import numpy as np

def create_features(df):
    """
    Apply feature engineering to the dataset.
    """
    df = df.copy()
    
    # Check if Timestamp is present
    if 'Timestamp' in df.columns:
        # Check if Timestamp is a string and handle it
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['hour'] = df['Timestamp'].dt.hour
        df['minute'] = df['Timestamp'].dt.minute
        df['time_in_hours'] = df['hour'] + df['minute'] / 60.0
        # We can drop original Timestamp after extracting features
        df = df.drop(columns=['Timestamp'])
    
    # Check if 'Time' is present
    if 'Time' in df.columns:
        try:
            time_dt = pd.to_datetime(df['Time'], format='%H:%M', errors='coerce')
            if time_dt.isna().all():
                time_dt = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')
            if 'hour' not in df.columns:
                df['hour'] = time_dt.dt.hour
                df['minute'] = time_dt.dt.minute
                df['time_in_hours'] = df['hour'] + df['minute'] / 60.0
        except Exception:
            pass
        # Drop original Time
        df = df.drop(columns=['Time'])
    
    # Ensure Day is numeric
    if 'Day' in df.columns:
        df['Day'] = pd.to_numeric(df['Day'], errors='coerce')
        # Fill missing Days with median if any
        df['Day'] = df['Day'].fillna(df['Day'].median())
    
    return df