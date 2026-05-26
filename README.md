# Smart Retail Assistant

Smart Retail Assistant is a FastAPI project for retail sales analysis. It combines a trained sales forecasting model, MongoDB-backed API endpoints, document search with RAG, and a small multi-agent layer for routing user questions.

## What It Does

- Ingests retail sales records into MongoDB.
- Predicts weekly sales using a saved scikit-learn model, with optional Azure ML endpoint inference.
- Explains predictions with Azure OpenAI.
- Searches retail PDF content through Azure OpenAI embeddings and ChromaDB.
- Routes questions to a Data Analyst Agent, Document Agent, or ML Expert Agent.
- Exposes a simple MCP tool layer for agent/tool communication.

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn backend.main:app --reload
```

Open the API docs:

```text
http://localhost:8000/docs
```

## Main Endpoints

| Endpoint | Method | Use |
| --- | --- | --- |
| `/` | GET | Health check |
| `/data-ingestion` | POST | Add sales records |
| `/sales-data` | GET | Read stored sales records |
| `/predict` | POST | Predict sales |
| `/search-documents` | POST | Search document chunks |
| `/ask` | POST | Ask a direct LLM question |
| `/multi-agent` | POST | Route a question to an agent |
| `/detect-anomalies` | GET | Return anomaly detection results |

## Project Layout

```text
backend/     FastAPI app and configuration
agents/      Agent prompts, router, MCP tool registry, MCP server
ml/          Preprocessing, training, and anomaly detection scripts
rag/         PDF indexing and ChromaDB retriever
data/        Retail dataset and generated outputs
tests/       Pytest API and ML tests
```

## Configuration

Create a local `.env` file with the services you use:

```env
MONGO_URI=your-mongodb-uri

AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-03-01-preview

AZURE_ML_ENDPOINT=your-azure-ml-endpoint
AZURE_ML_API_KEY=your-azure-ml-key
```

Do not submit `.env` with real keys.

## Tests

```bash
pytest
```

The tests cover the FastAPI routes and the basic ML workflow. Some runtime behavior still depends on local credentials and MongoDB availability.
