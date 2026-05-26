# MCP Setup

This project includes a small Model Context Protocol server so external clients can call the same tools used by the agents.

## Tools Exposed

| Tool | What it reads |
| --- | --- |
| `fetch_sales_data` | Recent records from `sales_data` in MongoDB |
| `fetch_predictions` | Recent records from `predictions` in MongoDB |
| `search_documents` | Relevant chunks from the RAG document index |

## Run The MCP Server

From the project root:

```bash
python agents/mcp_server.py
```

The server uses stdio, so it may keep running without printing much after startup. That is expected. An MCP client starts it and sends tool calls through the protocol.

## Desktop Example

Add a server entry similar to this in Desktop's config file:

```json
{
  "mcpServers": {
    "smart-retail": {
      "command": "python",
      "args": ["d:\\Project\\agents\\mcp_server.py"],
      "env": {
        "MONGO_URI": "your-mongodb-connection-string",
        "AZURE_OPENAI_ENDPOINT": "https://your-resource.openai.azure.com/",
        "AZURE_OPENAI_API_KEY": "your-key",
        "AZURE_OPENAI_DEPLOYMENT": "gpt-4o-mini",
        "AZURE_OPENAI_API_VERSION": "2024-03-01-preview"
      }
    }
  }
}
```

Restart Claude Desktop after changing the config.

## Troubleshooting

- If the server cannot import project modules, run it from `d:\Project`.
- If MongoDB tools fail, check `MONGO_URI`.
- If document search fails, rebuild the vector store and confirm Azure OpenAI embedding settings.
- If the MCP package is missing, install dependencies from `requirements.txt`.
