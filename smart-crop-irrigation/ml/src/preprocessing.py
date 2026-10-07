import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from feature_engineering import create_features

def load_and_preprocess_data(filepath):
    # Load dataset
    df = pd.read_excel(filepath)
    
    # Feature engineering
    df = create_features(df)
    
    # Handle missing values if any
    # Forward fill or drop, here we'll just drop for simplicity or fill with median
    # Let's fill numerical columns with median just in case
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    # Ensure Pump_Status is the target and drop NA from target
    if 'Pump_Status' in df.columns:
        df = df.dropna(subset=['Pump_Status'])
        
    return df

def get_train_test_data(df, target_col='Pump_Status', test_size=0.20, random_state=42):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    return X_train, X_test, y_train, y_test

def get_scaler(X_train):
    scaler = StandardScaler()
    scaler.fit(X_train)
    return scaler