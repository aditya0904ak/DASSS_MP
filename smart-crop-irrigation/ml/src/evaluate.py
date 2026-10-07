import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import os

def evaluate_model(model_name, y_true, y_pred):
    """
    Evaluates a model and returns metrics.
    """
    accuracy = accuracy_score(y_true, y_pred)
    # Target class is 1 (Pump ON)
    precision = precision_score(y_true, y_pred, pos_label=1, zero_division=0)
    recall = recall_score(y_true, y_pred, pos_label=1, zero_division=0)
    f1 = f1_score(y_true, y_pred, pos_label=1, zero_division=0)
    
    cm = confusion_matrix(y_true, y_pred)
    cr = classification_report(y_true, y_pred, zero_division=0)
    
    metrics = {
        'model': model_name,
        'accuracy': accuracy,
        'precision_class1': precision,
        'recall_class1': recall,
        'f1_class1': f1,
        'confusion_matrix': cm,
        'classification_report': cr
    }
    
    return metrics

def plot_confusion_matrix(cm, model_name, output_dir='models'):
    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix: {model_name}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    # Save the plot
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f'cm_{model_name.replace(" ", "_")}.png'))
    plt.close()