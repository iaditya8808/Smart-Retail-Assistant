import logging
from typing import Any, Callable, Dict, List


logger = logging.getLogger(__name__)


def fetch_sales_data() -> str:
    logger.info("MCP tool: fetch_sales_data")

    try:
        from agents.tools import fetch_sales_data as tool
    except ModuleNotFoundError:
        from tools import fetch_sales_data as tool

    return tool()


def fetch_predictions() -> str:
    logger.info("MCP tool: fetch_predictions")

    try:
        from agents.tools import fetch_predictions as tool
    except ModuleNotFoundError:
        from tools import fetch_predictions as tool

    return tool()


def search_documents(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    logger.info(f"MCP tool: search_documents query={query!r}")

    from rag.retriever import retriever

    docs = retriever.invoke(query)

    return [
        {
            "content": doc.page_content,
            "metadata": getattr(doc, "metadata", {}),
        }
        for doc in docs[:top_k]
    ]


MCP_TOOLS: Dict[str, Dict[str, Any]] = {
    "fetch_sales_data": {
        "description": "Fetch recent retail sales records from MongoDB.",
        "handler": fetch_sales_data,
    },
    "fetch_predictions": {
        "description": "Fetch recent sales prediction records from MongoDB.",
        "handler": fetch_predictions,
    },
    "search_documents": {
        "description": "Search indexed retail documents using the RAG retriever.",
        "handler": search_documents,
    },
}


def list_mcp_tools() -> List[Dict[str, str]]:
    return [
        {
            "name": name,
            "description": tool["description"],
        }
        for name, tool in MCP_TOOLS.items()
    ]


def call_mcp_tool(tool_name: str, **kwargs: Any) -> Any:
    """Call a registered Smart Retail MCP-style tool."""
    tool = MCP_TOOLS.get(tool_name)

    if tool is None:
        raise ValueError(f"Unknown MCP tool: {tool_name}")

    handler: Callable[..., Any] = tool["handler"]
    return handler(**kwargs)
