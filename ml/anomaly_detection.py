import os

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest


data_path = os.path.join("data", "cleaned_retail_sales.csv")
df = pd.read_csv(data_path)
print(f"Loaded data from {data_path}")

feature_columns = [
    "Weekly_Sales",
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment",
]

X = df[feature_columns]

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42,
)

model.fit(X)

df["anomaly"] = model.predict(X)
df["anomaly"] = df["anomaly"].map({
    1: "Normal",
    -1: "Anomaly",
})

model_path = os.path.join("ml", "anomaly_model.pkl")
joblib.dump(model, model_path)
print(f"Anomaly model saved to {model_path}")

results_path = os.path.join("data", "anomaly_results.csv")
df.to_csv(results_path, index=False)
print(f"Anomaly results saved to {results_path}")

print("\n--- Anomaly Detection Completed ---")
print(df["anomaly"].value_counts())
