# ML Pipeline for IoT-Based Smart Crop Water Management

This directory contains the machine learning training pipeline for predicting irrigation requirements based on environmental sensor data.

## 1. Dataset Description
The model is trained on the `Edge_IoT_Predictive_Irrigation_Dataset.xlsx` dataset, which contains 960 observations of environmental parameters and the corresponding pump status. 

## 2. Features Used
The following features are extracted and used for training:
- `Temperature_C`
- `Humidity_pct`
- `Soil_Moisture_pct`
- `Light_Intensity`
- `Day` (numeric)
- `hour` (extracted from time)
- `minute` (extracted from time)
- `time_in_hours` (hour + minute/60.0)

## 3. Target Variable
- **Target**: `Pump_Status`
- **Classes**: 
  - `0` = Pump OFF
  - `1` = Pump ON (Irrigation required)

## 4. Preprocessing
- Time/Timestamp columns are parsed to extract numeric features (`hour`, `minute`, `time_in_hours`).
- Numerical missing values (if any) are filled with the median.
- For Logistic Regression, features are scaled using `StandardScaler`.
- The dataset is split into training and testing sets using a stratified split (80/20) to ensure the proportion of `Pump_Status` is maintained in both sets.

## 5. Class Imbalance Issue
The target variable `Pump_Status` is highly imbalanced in the dataset:
- **Class 0 (Pump OFF)**: 932 samples (97.08%)
- **Class 1 (Pump ON)**: 28 samples (2.92%)

Due to this significant imbalance, relying solely on **Accuracy** is misleading. A naive model that always predicts "Pump OFF" would still achieve ~97% accuracy without learning anything. Therefore, we focus on **Precision, Recall, and F1-Score specifically for Class 1**. We also use `class_weight='balanced'` when instantiating the models to penalize misclassifications of the minority class more heavily.

## 6. Models Trained
We trained and compared three models:
1. Logistic Regression
2. Decision Tree
3. Random Forest

## 7. Evaluation Metrics (Actual Results)

| Model | Accuracy | Precision (Class 1) | Recall (Class 1) | F1-Score (Class 1) |
|-------|----------|---------------------|------------------|--------------------|
| Logistic Regression | 0.9167 | 0.2727 | 1.0000 | 0.4286 |
| Decision Tree | 0.9948 | 0.8571 | 1.0000 | 0.9231 |
| Random Forest | 0.9948 | 0.8571 | 1.0000 | 0.9231 |

## 8. Best Model Selection
**Best Model**: Decision Tree 

**Why it was selected**: The Decision Tree and Random Forest achieved identical top performance. Both models perfectly recalled all instances of required irrigation (Recall = 1.0) and maintained high precision (0.8571), leading to an F1-Score of 0.9231 for Class 1. Given the tie in performance, the **Decision Tree** was selected as the final model because it is simpler, faster for edge/IoT inference, and highly interpretable. It ensures we don't miss any required watering while keeping false positives reasonably low. 

*(Note: Random Forest could also be used with identical performance, but Decision Tree is preferred here for its lightweight nature on edge devices).*

## 9. How to Train
To execute the training pipeline and generate the model artifacts:

```bash
# 1. Install dependencies
pip install -r ml/requirements.txt

# 2. Run the training script
python ml/src/train.py
```
This will train the models, output the metrics, generate confusion matrices in `ml/models/`, and save the best model to `ml/models/irrigation_model.pkl` along with `scaler.pkl` and `feature_names.pkl`.

## 10. How to Make a Prediction
To make a prediction, you can run the `predict.py` script or use its function in your application:

```bash
python ml/src/predict.py
```

**Python Usage:**
```python
from ml.src.predict import predict_irrigation

sensor_data = {
    "Temperature_C": 30.0,
    "Humidity_pct": 40.0,
    "Soil_Moisture_pct": 25.0,
    "Light_Intensity": 1000,
    "Day": 1,
    "Time": "12:00:00"
}

result = predict_irrigation(sensor_data)
print(result)
# Expected Output: {'pump_prediction': 0, 'irrigation_required': False, 'confidence': 1.0}
```

*Note: The current phase focuses on ML prediction. In the final architecture, these predictions should be validated against hardware safety rules before physically switching the relay.*
