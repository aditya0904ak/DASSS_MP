import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from preprocessing import load_and_preprocess_data, get_train_test_data, get_scaler
from evaluate import evaluate_model, plot_confusion_matrix

def main():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Edge_IoT_Predictive_Irrigation_Dataset.xlsx')
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # 1. Load and Preprocess
    print("Loading dataset...")
    df_raw = pd.read_excel(data_path)
    print("Original Dataset Shape:", df_raw.shape)
    print("Original Columns:", df_raw.columns.tolist())
    print("Missing Values in raw data:\n", df_raw.isna().sum())
    
    if 'Pump_Status' in df_raw.columns:
        print("\nClass Distribution (Pump_Status):")
        print(df_raw['Pump_Status'].value_counts())
        print(df_raw['Pump_Status'].value_counts(normalize=True) * 100)
    
    df = load_and_preprocess_data(data_path)
    print("\nProcessed Dataset Shape:", df.shape)
    print("Processed Features:", df.columns.tolist())
    
    # 2. Split Data
    X_train, X_test, y_train, y_test = get_train_test_data(df)
    
    # 3. Scaling
    scaler = get_scaler(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save scaler and feature names
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    joblib.dump(list(X_train.columns), os.path.join(models_dir, 'feature_names.pkl'))
    
    # 4. Initialize Models
    models = {
        'Logistic Regression': LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(class_weight='balanced', random_state=42, max_depth=5),
        'Random Forest': RandomForestClassifier(class_weight='balanced', random_state=42, n_estimators=100)
    }
    
    results = []
    best_f1 = -1
    best_model = None
    best_model_name = ""
    
    # 5. Train and Evaluate
    for name, model in models.items():
        print(f"\nTraining {name}...")
        if name == 'Logistic Regression':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
        metrics = evaluate_model(name, y_test, y_pred)
        results.append(metrics)
        
        plot_confusion_matrix(metrics['confusion_matrix'], name, output_dir=models_dir)
        
        print(f"Metrics for {name}:")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision (Class 1): {metrics['precision_class1']:.4f}")
        print(f"  Recall (Class 1):    {metrics['recall_class1']:.4f}")
        print(f"  F1-Score (Class 1):  {metrics['f1_class1']:.4f}")
        print("Classification Report:\n", metrics['classification_report'])
        
        # Select best model based on F1-Score of Class 1
        if metrics['f1_class1'] > best_f1:
            best_f1 = metrics['f1_class1']
            best_model = model
            best_model_name = name

    # 6. Save Best Model
    print(f"\nBest Model selected: {best_model_name} with F1-Score: {best_f1:.4f}")
    best_model_path = os.path.join(models_dir, 'irrigation_model.pkl')
    # Save the pipeline/dict so predict.py knows if it needs scaling
    model_data = {
        'model_name': best_model_name,
        'model': best_model,
        'requires_scaling': best_model_name == 'Logistic Regression'
    }
    joblib.dump(model_data, best_model_path)
    print(f"Saved best model to {best_model_path}")

if __name__ == '__main__':
    main()