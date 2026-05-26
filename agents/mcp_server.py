#!/usr/bin/env python
"""MCP entry point for Smart Retail Assistant tools."""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path

from mcp.server import Server
from mcp.types import TextContent, Tool

from langchain_openai import AzureChatOpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.mcp_context import (
    MCP_TOOLS,
    fetch_predictions,
    fetch_sales_data,
    search_documents,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-retail-mcp")

try:
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-03-01-preview"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
        temperature=0,
    )
    logger.info("Azure OpenAI connected")
except Exception as exc:
    logger.warning(f"Azure OpenAI not available: {exc}")
    llm = None

server = Server("smart-retail-assistant")


@server.list_tools()
async def list_tools():
    """Return the tool definitions exposed to MCP clients."""
    tools = []

    for tool_name, tool_info in MCP_TOOLS.items():
        tools.append(
            Tool(
                name=tool_name,
                description=tool_info["description"],
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search text used by search_documents",
                        }
                    },
                },
            )
        )

    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute a Smart Retail tool through the MCP interface."""
    logger.info(f"MCP tool call: {name}")

    try:
        if name == "fetch_sales_data":
            result = fetch_sales_data()
        elif name == "fetch_predictions":
            result = fetch_predictions()
        elif name == "search_documents":
            query = arguments.get("query", "")
            result = json.dumps(search_documents(query), indent=2)
        else:
            return [TextContent(type="text", text=f"Tool '{name}' not found")]

        if llm and name != "fetch_sales_data":
            try:
                prompt = f"Summarize this retail data and list the main business insight:\n\n{result}"
                response = llm.invoke(prompt)
                result = f"{result}\n\nAI insight:\n{response.content}"
            except Exception as exc:
                logger.warning(f"Azure summary failed: {exc}")

        return [TextContent(type="text", text=str(result))]

    except Exception as exc:
        logger.error(f"Tool execution error: {exc}")
        return [TextContent(type="text", text=f"Error: {exc}")]


async def main():
    """Start the MCP server."""
    logger.info("Starting Smart Retail MCP server")
    logger.info("Tools: fetch_sales_data, fetch_predictions, search_documents")

    async with server:
        logger.info("MCP server is running")
        await asyncio.sleep(float("inf"))


if __name__ == "__main__":
    asyncio.run(main())
