import pandas as pd

df = pd.read_excel('d:/DASSS_MP/smart-crop-irrigation/ml/data/Edge_IoT_Predictive_Irrigation_Dataset.xlsx')
pump_on = df[df['Pump_Status'] == 1]
print("Total rows:", len(df))
print("Pump_Status == 1 rows count:", len(pump_on))
print("\nPump_Status == 1 details:")
print(pump_on[['Timestamp', 'Day', 'Time', 'Temperature_C', 'Humidity_pct', 'Soil_Moisture_pct', 'Light_Intensity', 'Pump_Status']].to_string())

print("\nSummary statistics of Pump_Status == 1:")
print(pump_on[['Temperature_C', 'Humidity_pct', 'Soil_Moisture_pct', 'Light_Intensity']].describe())

print("\nSummary statistics of Pump_Status == 0:")
print(df[df['Pump_Status'] == 0][['Temperature_C', 'Humidity_pct', 'Soil_Moisture_pct', 'Light_Intensity']].describe())
