import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


data_path = os.path.join("data", "cleaned_retail_sales.csv")
df = pd.read_csv(data_path)
print(f"Loaded data from {data_path}")

feature_columns = [
    "Store",
    "Holiday_Flag",
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment",
    "day",
    "month",
    "year",
]

X = df[feature_columns]
y = df["Weekly_Sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)
print("Random Forest training completed")

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, predictions)

print("\n--- Model Performance ---")
print(f"MAE:      {mae:.2f}")
print(f"MSE:      {mse:.2f}")
print(f"RMSE:     {rmse:.2f}")
print(f"R2 Score: {r2:.4f}")
print(f"Accuracy: {r2 * 100:.2f}%")

model_path = os.path.join("ml", "model.pkl")
joblib.dump(model, model_path)
print(f"\nModel saved to {model_path}")
