#  Smart Retail Assistant

An AI-powered retail analytics platform that combines predictive modeling, intelligent document search, and multi-agent routing to deliver actionable business insights.

##  Features

- **Sales Forecasting** – Predict weekly sales using trained scikit-learn models with Azure ML integration
- **Multi-Agent System** – Route questions to specialized agents (Data Analyst, Document Expert, ML Specialist)
- **Document Search** – Intelligent RAG-powered search over retail PDFs using Azure OpenAI embeddings
- **Anomaly Detection** – Automatically detect unusual sales patterns
- **MongoDB Integration** – Persistent storage of sales records and analysis results
- **FastAPI** – High-performance REST API with automatic interactive docs
- **MCP Tools** – Model Context Protocol layer for seamless agent-tool communication

##  Quick Start

### Prerequisites

- Python 3.11+
- MongoDB (local or cloud)
- Azure OpenAI (optional, for LLM features)
- Azure ML (optional, for advanced inference)

### Installation

1. **Clone and navigate:**
```bash
cd Smart\ Retail\ Assistant
```

2. **Create virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** (see [Configuration](#configuration) below)

5. **Run the API:**
```bash
uvicorn backend.main:app --reload
```

6. **Explore the API:**
Open http://localhost:8000/docs in your browser for interactive API documentation.

##  API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/data-ingestion` | POST | Ingest sales records into MongoDB |
| `/sales-data` | GET | Retrieve stored sales records |
| `/predict` | POST | Forecast weekly sales |
| `/search-documents` | POST | Search retail PDFs using RAG |
| `/ask` | POST | Direct LLM question answering |
| `/multi-agent` | POST | Route question to specialized agent |
| `/detect-anomalies` | GET | Get anomaly detection results |

##  Configuration

Create a `.env` file in the project root with your service credentials:

```env
# MongoDB
MONGO_URI=your-mongodb-connection-string

# Azure OpenAI (for LLM and embeddings)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-03-01-preview

# Azure ML (optional, for advanced inference)
AZURE_ML_ENDPOINT=your-ml-endpoint
AZURE_ML_API_KEY=your-ml-api-key
```

 **Never commit `.env` with real credentials.** Add it to `.gitignore`.

##  Project Structure

```
backend/          FastAPI application and configuration
agents/           Multi-agent system, routing logic, and MCP tools
ml/               Model training, preprocessing, anomaly detection
rag/              PDF indexing, embeddings, and ChromaDB retriever
data/             Retail datasets and analysis outputs
tests/            Unit tests for API and ML components
uploads/          Temporary storage for file uploads
```

##  Testing

Run the test suite:

```bash
pytest
```

Tests cover API routes, ML workflows, and data processing. Some tests require live MongoDB and Azure credentials.

##  Documentation

- **[Deployment Architecture](DEPLOYMENT_ARCHITECTURE.md)** – System design and cloud topology
- **[Manual Azure Deployment](MANUAL_AZURE_DEPLOYMENT.md)** – Step-by-step Azure App Service setup
- **[MCP Setup Guide](MCP_SETUP.md)** – Model Context Protocol configuration
- **[Testing Guide](TESTING.md)** – Detailed test instructions

##  Technology Stack

- **Framework:** FastAPI, Uvicorn
- **AI/ML:** LangChain, scikit-learn, Azure OpenAI, pandas, numpy
- **Database:** MongoDB
- **Vector Search:** ChromaDB, Azure OpenAI Embeddings
- **Document Processing:** Azure Document Intelligence
- **Cloud:** Microsoft Azure (App Service, OpenAI, ML Services)
- **Testing:** pytest

##  Usage Examples

### Predict Sales
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"features": [100, 200, 300, 400]}
)
print(response.json())
```

### Search Documents
```python
response = requests.post(
    "http://localhost:8000/search-documents",
    json={"query": "holiday promotion impact"}
)
print(response.json())
```

### Ask Multi-Agent
```python
response = requests.post(
    "http://localhost:8000/multi-agent",
    json={"question": "What caused the sales spike in Q3?"}
)
print(response.json())
```

> **Tip:** Use the interactive API docs at http://localhost:8000/docs to test endpoints directly in your browser.

##  Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | Ensure virtual environment is activated and `pip install -r requirements.txt` is run |
| MongoDB connection fails | Verify `MONGO_URI` in `.env` and network connectivity |
| Azure OpenAI errors | Check API key, endpoint, and deployment name in `.env` |
| Port 8000 already in use | Change port: `uvicorn backend.main:app --port 8001` |

##  License

[Specify your license here]

##  Contributing

Contributions welcome! Please create a feature branch and submit a pull request.

##  Support

For issues and questions, please open an issue on this repository.
