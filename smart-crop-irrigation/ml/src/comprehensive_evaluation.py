import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import (
    confusion_matrix, classification_report,
    precision_score, recall_score, f1_score,
    balanced_accuracy_score, accuracy_score
)
from preprocessing import load_and_preprocess_data, get_train_test_data

def evaluate_production_model():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Edge_IoT_Predictive_Irrigation_Dataset.xlsx')
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    
    df = load_and_preprocess_data(data_path)
    X_train, X_test, y_train, y_test = get_train_test_data(df, random_state=42)
    
    model_data = joblib.load(os.path.join(models_dir, 'irrigation_model.pkl'))
    model = model_data['model']
    
    y_pred = model.predict(X_test)
    
    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    bal_acc = balanced_accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    weighted_f1 = f1_score(y_test, y_pred, average='weighted')
    
    prec_0 = precision_score(y_test, y_pred, pos_label=0)
    rec_0 = recall_score(y_test, y_pred, pos_label=0)
    f1_0 = f1_score(y_test, y_pred, pos_label=0)
    
    prec_1 = precision_score(y_test, y_pred, pos_label=1)
    rec_1 = recall_score(y_test, y_pred, pos_label=1)
    f1_1 = f1_score(y_test, y_pred, pos_label=1)
    
    print("=== MODEL EVALUATION METRICS ===")
    print(f"Total Test Samples: {len(y_test)}")
    print(f"Class 0 (Pump OFF) in Test: {sum(y_test == 0)}")
    print(f"Class 1 (Pump ON) in Test:  {sum(y_test == 1)}")
    print("\nConfusion Matrix [ [TN, FP], [FN, TP] ]:")
    print(cm)
    print("\n--- Metrics Summary ---")
    print(f"Overall Accuracy:        {acc:.4f} ({acc*100:.2f}%)")
    print(f"Balanced Accuracy:       {bal_acc:.4f} ({bal_acc*100:.2f}%)")
    print(f"Macro F1-Score:          {macro_f1:.4f}")
    print(f"Weighted F1-Score:       {weighted_f1:.4f}")
    print("\n--- Per-Class Metrics ---")
    print(f"Class 0 (Pump OFF):  Precision={prec_0:.4f}, Recall={rec_0:.4f}, F1={f1_0:.4f}")
    print(f"Class 1 (Pump ON):   Precision={prec_1:.4f}, Recall={rec_1:.4f}, F1={f1_1:.4f}")
    print("\nFull Classification Report:")
    print(classification_report(y_test, y_pred, digits=4))

if __name__ == '__main__':
    evaluate_production_model()
