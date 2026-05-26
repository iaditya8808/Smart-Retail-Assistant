import logging
import os

from langchain_openai import AzureChatOpenAI

from agents.mcp_context import call_mcp_tool
from agents.prompts import DATA_ANALYST_PROMPT


logger = logging.getLogger(__name__)
_llm = None


def _get_llm():
    global _llm

    if _llm is None:
        try:
            _llm = AzureChatOpenAI(
                api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                temperature=0,
            )
        except Exception as exc:
            logger.error(f"Failed to initialize Azure OpenAI: {exc}")
            return None

    return _llm


def run_data_analyst_agent(user_query: str) -> str:
    llm = _get_llm()
    if llm is None:
        return "Error: Azure OpenAI not configured properly"

    sales_data = call_mcp_tool("fetch_sales_data")

    prompt = f"""{DATA_ANALYST_PROMPT}

Question:
{user_query}

Recent sales records:
{sales_data}
"""

    return llm.invoke(prompt).content
