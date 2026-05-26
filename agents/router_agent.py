from typing import Any, Dict

from agents.data_analyst_agent import run_data_analyst_agent
from agents.document_agent import run_document_agent
from agents.ml_expert_agent import run_ml_expert_agent


DOCUMENT_TERMS = {
    "policy",
    "document",
    "insurance",
    "rules",
    "terms",
    "agreement",
    "contract",
}

ML_TERMS = {
    "predict",
    "prediction",
    "forecast",
    "model",
    "sales forecast",
    "revenue forecast",
    "estimate",
}


def route_query(user_query: str) -> Dict[str, Any]:
    query = user_query.lower()

    if any(term in query for term in DOCUMENT_TERMS):
        return {
            "agent": "Document Agent",
            "agent_type": "document",
            "response": run_document_agent(user_query),
            "query": user_query,
        }

    if any(term in query for term in ML_TERMS):
        return {
            "agent": "ML Expert Agent",
            "agent_type": "ml_expert",
            "response": run_ml_expert_agent(user_query),
            "query": user_query,
        }

    return {
        "agent": "Data Analyst Agent",
        "agent_type": "data_analyst",
        "response": run_data_analyst_agent(user_query),
        "query": user_query,
    }
