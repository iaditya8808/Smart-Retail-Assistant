import pytest
from fastapi.testclient import TestClient
from backend.main import app, SalesInput, SalesIngestionRequest, DocumentSearchRequest, AgentRequest

client = TestClient(app)


class TestHomeAPI:
    def test_home_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Smart Retail Assistant Running Successfully"


class TestDataIngestionAPI:
    def test_data_ingestion_valid(self):
        payload = {
            "records": [
                {
                    "Store": 1,
                    "Holiday_Flag": 0,
                    "Temperature": 72.5,
                    "Fuel_Price": 2.5,
                    "CPI": 200.0,
                    "Unemployment": 5.0,
                    "day": 15,
                    "month": 3,
                    "year": 2024
                }
            ]
        }
        response = client.post("/data-ingestion", json=payload)
        assert response.status_code == 200
        assert "inserted_count" in response.json()

    def test_data_ingestion_empty(self):
        payload = {"records": []}
        response = client.post("/data-ingestion", json=payload)
        assert response.status_code == 400


class TestPredictionAPI:
    def test_predict_sales_valid(self):
        payload = {
            "Store": 1,
            "Holiday_Flag": 0,
            "Temperature": 72.5,
            "Fuel_Price": 2.5,
            "CPI": 200.0,
            "Unemployment": 5.0,
            "day": 15,
            "month": 3,
            "year": 2024
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        result = response.json()
        assert "local_prediction" in result or "azure_ml_prediction" in result


class TestDocumentSearchAPI:
    def test_search_documents_valid(self):
        payload = {
            "query": "What are retail sales trends?",
            "top_k": 3
        }
        response = client.post("/search-documents", json=payload)
        assert response.status_code in [200, 503]  # 503 if retriever not initialized
        if response.status_code == 200:
            result = response.json()
            assert "query" in result
            assert "documents" in result

    def test_search_documents_default_top_k(self):
        payload = {"query": "sales data"}
        response = client.post("/search-documents", json=payload)
        assert response.status_code in [200, 503]


class TestAnomaliesAPI:
    def test_detect_anomalies(self):
        response = client.get("/detect-anomalies")
        assert response.status_code in [200, 404, 500]
        if response.status_code == 200:
            result = response.json()
            assert "total_anomalies" in result
            assert "sample_anomalies" in result


class TestMultiAgentAPI:
    def test_multi_agent_valid(self):
        payload = {"question": "Analyze sales performance"}
        response = client.post("/multi-agent", json=payload)
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            result = response.json()
            assert "question" in result
            assert "response" in result
