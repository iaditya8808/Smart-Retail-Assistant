# Deployment Architecture

The backend can run locally or be deployed as an Azure App Service. The same FastAPI app serves prediction, document search, agent routing, and MCP-tool discovery routes.

## Runtime View

```text
User or API client
        |
        v
FastAPI backend
        |
        +-- MongoDB: sales records and prediction history
        +-- Local model files: Random Forest and anomaly detector
        +-- Azure ML endpoint: optional hosted prediction
        +-- Azure OpenAI: explanations, agents, embeddings
        +-- ChromaDB: local vector store for document retrieval
        +-- Azure Document Intelligence: optional PDF text extraction
```

## Azure Components

- Azure OpenAI is used for LLM responses and embeddings.
- Azure ML is supported through the prediction endpoint when endpoint credentials are present.
- Azure App Service can host the FastAPI backend.
- Azure Document Intelligence is wired as an optional document extraction service.

## Security Notes

- Keep keys in `.env` for local work only.
- Use Azure Key Vault or App Service application settings in deployment.
- Do not commit `.env`, model credentials, or database connection strings.
- Use HTTPS for deployed API traffic.
- Restrict MongoDB access to trusted networks where possible.
