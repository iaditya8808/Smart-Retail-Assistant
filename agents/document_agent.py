import logging
import os

from langchain_openai import AzureChatOpenAI


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


def run_document_agent(query: str) -> str:
    llm = _get_llm()
    if llm is None:
        return "Error: Azure OpenAI not configured"

    try:
        from agents.mcp_context import call_mcp_tool

        docs = call_mcp_tool("search_documents", query=query, top_k=3)
        context = "\n\n".join(doc["content"] for doc in docs)

        prompt = f"""
Use the document context below to answer the question.
If the answer is not in the context, say the indexed documents do not include it.

Context:
{context}

Question:
{query}
"""

        return llm.invoke(prompt).content

    except Exception as exc:
        logger.error(f"Document agent error: {exc}")
        return f"Error: {exc}"
