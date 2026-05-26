import pytest
import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


class TestMLModels:
    """Test suite for ML models"""

    @pytest.fixture
    def sample_data(self):
        """Create sample retail sales data for testing"""
        data = {
            "Store": [1, 2, 3, 1, 2, 3],
            "Holiday_Flag": [0, 1, 0, 0, 1, 0],
            "Temperature": [72.5, 75.0, 68.0, 70.0, 76.0, 69.0],
            "Fuel_Price": [2.5, 2.6, 2.4, 2.5, 2.6, 2.4],
            "CPI": [200.0, 205.0, 195.0, 200.0, 205.0, 195.0],
            "Unemployment": [5.0, 5.5, 4.8, 5.0, 5.5, 4.8],
            "day": [15, 20, 10, 15, 20, 10],
            "month": [3, 6, 9, 3, 6, 9],
            "year": [2024, 2024, 2024, 2024, 2024, 2024],
            "Weekly_Sales": [50000, 55000, 45000, 50000, 55000, 45000]
        }
        return pd.DataFrame(data)

    def test_model_training(self, sample_data):
        """Test Random Forest model training"""
        X = sample_data[[
            "Store", "Holiday_Flag", "Temperature", "Fuel_Price",
            "CPI", "Unemployment", "day", "month", "year"
        ]]
        y = sample_data["Weekly_Sales"]

        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)

        assert model is not None
        assert hasattr(model, "predict")
        assert len(model.feature_importances_) == X.shape[1]

    def test_model_prediction(self, sample_data):
        """Test model prediction on new data"""
        X = sample_data[[
            "Store", "Holiday_Flag", "Temperature", "Fuel_Price",
            "CPI", "Unemployment", "day", "month", "year"
        ]]
        y = sample_data["Weekly_Sales"]

        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)

        test_sample = np.array([[1, 0, 72.5, 2.5, 200.0, 5.0, 15, 3, 2024]])
        prediction = model.predict(test_sample)

        assert prediction is not None
        assert len(prediction) == 1
        assert prediction[0] > 0

    def test_model_persistence(self, sample_data, tmp_path):
        """Test model saving and loading"""
        X = sample_data[[
            "Store", "Holiday_Flag", "Temperature", "Fuel_Price",
            "CPI", "Unemployment", "day", "month", "year"
        ]]
        y = sample_data["Weekly_Sales"]

        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)

        # Save model
        model_path = tmp_path / "test_model.pkl"
        joblib.dump(model, model_path)

        # Load model
        loaded_model = joblib.load(model_path)

        # Test both models produce same predictions
        test_sample = np.array([[1, 0, 72.5, 2.5, 200.0, 5.0, 15, 3, 2024]])
        pred1 = model.predict(test_sample)
        pred2 = loaded_model.predict(test_sample)

        assert np.allclose(pred1, pred2)

    def test_train_test_split(self, sample_data):
        """Test train/test split for model validation"""
        X = sample_data[[
            "Store", "Holiday_Flag", "Temperature", "Fuel_Price",
            "CPI", "Unemployment", "day", "month", "year"
        ]]
        y = sample_data["Weekly_Sales"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        assert X_train.shape[0] + X_test.shape[0] == X.shape[0]
        assert X_train.shape[1] == X.shape[1]

    def test_model_file_exists(self):
        """Test if trained models exist"""
        model_paths = ["ml/model.pkl", "ml/anomaly_model.pkl"]

        for path in model_paths:
            if os.path.exists(path):
                assert os.path.getsize(path) > 0, f"{path} is empty"
            else:
                pytest.skip(f"{path} not found (models may not be trained yet)")

    def test_feature_engineering(self, sample_data):
        """Test feature engineering preprocessing"""
        features = ["Store", "Holiday_Flag", "Temperature", "Fuel_Price",
                    "CPI", "Unemployment", "day", "month", "year"]

        # Check all features exist
        for feature in features:
            assert feature in sample_data.columns

        # Check no null values
        assert sample_data[features].isnull().sum().sum() == 0

        # Check data types
        assert sample_data["Store"].dtype == np.int64
        assert sample_data["Temperature"].dtype == np.float64
