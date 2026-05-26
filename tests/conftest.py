"""Pytest configuration and fixtures for Smart Retail Assistant"""

import pytest
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def test_config():
    """Test configuration fixture"""
    return {
        "db_uri": "mongodb://localhost:27017",
        "db_name": "test_retail_db",
        "api_timeout": 30
    }


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables for testing"""
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com/")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-key-123")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "test-deployment")
    monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    monkeypatch.setenv("MONGO_URI", "mongodb://localhost:27017")
    return monkeypatch
