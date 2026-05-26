
try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except Exception:
    pass

import logging
import os
import sys

from typing import List, Optional

import joblib
import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel
from pymongo import MongoClient

from agents.router_agent import route_query
from rag.retriever import retriever


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stdout,
    force=True,
)

logger = logging.getLogger(__name__)
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

AZURE_ML_ENDPOINT = os.getenv("AZURE_ML_ENDPOINT")
AZURE_ML_API_KEY = os.getenv("AZURE_ML_API_KEY")


try:
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential

    doc_intel_client = None
    doc_intel_endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    doc_intel_key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_API_KEY")

    if doc_intel_endpoint and doc_intel_key:
        doc_intel_client = DocumentIntelligenceClient(
            endpoint=doc_intel_endpoint,
            credential=AzureKeyCredential(doc_intel_key),
        )
except Exception as exc:
    logger.warning(f"Document Intelligence not available: {exc}")
    doc_intel_client = None


_db = None


def get_db():
    global _db

    if _db is None:
        try:
            client = MongoClient(
                os.getenv("MONGO_URI"),
                serverSelectionTimeoutMS=5000,
            )
            client.admin.command("ping")
            _db = client["smart_retail_db"]
        except Exception as exc:
            logger.error(f"MongoDB Error: {exc}")
            return None

    return _db


try:
    model = joblib.load("ml/model.pkl")
except Exception as exc:
    logger.error(f"Model Loading Error: {exc}")
    model = None


try:
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        temperature=0,
    )
except Exception as exc:
    logger.error(f"Azure OpenAI Error: {exc}")
    llm = None


qa_chain = llm if llm is not None and retriever is not None else None

app = FastAPI(
    title="Smart Retail Assistant API",
    version="1.0",
)


class SalesInput(BaseModel):
    Store: int
    Holiday_Flag: int
    Temperature: float
    Fuel_Price: float
    CPI: float
    Unemployment: float
    day: int
    month: int
    year: int


class SalesIngestionRequest(BaseModel):
    records: List[SalesInput]


class DocumentSearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3


class AgentRequest(BaseModel):
    question: str


@app.get("/")
def home():
    logger.info("GET /")
    return {"message": "Smart Retail Assistant Running Successfully"}


@app.post("/predict")
def predict_sales(data: SalesInput):
    logger.info("POST /predict")

    try:
        db = get_db()
        if db is None:
            return {"error": "Database connection failed"}

        azure_prediction = None

        if AZURE_ML_ENDPOINT and AZURE_ML_API_KEY:
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {AZURE_ML_API_KEY}",
                }

                payload = {
                    "Inputs": {
                        "input1": [
                            {
                                "Store": data.Store,
                                "Holiday_Flag": data.Holiday_Flag,
                                "Temperature": data.Temperature,
                                "Fuel_Price": data.Fuel_Price,
                                "CPI": data.CPI,
                                "Unemployment": data.Unemployment,
                                "Date": f"{data.year}-{data.month:02d}-{data.day:02d}",
                                "year": data.year,
                                "month": data.month,
                                "day": data.day,
                            }
                        ]
                    }
                }

                response = requests.post(
                    AZURE_ML_ENDPOINT,
                    json=payload,
                    headers=headers,
                    timeout=60,
                )
                azure_prediction = response.json()
            except Exception as exc:
                logger.error(f"Azure ML Error: {exc}")

        local_prediction = None

        if model is not None:
            features = np.array(
                [
                    [
                        data.Store,
                        data.Holiday_Flag,
                        data.Temperature,
                        data.Fuel_Price,
                        data.CPI,
                        data.Unemployment,
                        data.day,
                        data.month,
                        data.year,
                    ]
                ]
            )
            local_prediction = float(model.predict(features)[0])

        final_prediction = azure_prediction if azure_prediction is not None else local_prediction
        ai_explanation = "Azure OpenAI not initialized"

        if llm is not None:
            prompt = f"""
Explain this retail sales prediction in simple business terms.

Prediction:
{final_prediction}

Input:
Store={data.Store}
Holiday_Flag={data.Holiday_Flag}
Temperature={data.Temperature}
Fuel_Price={data.Fuel_Price}
CPI={data.CPI}
Unemployment={data.Unemployment}
Date={data.year}-{data.month:02d}-{data.day:02d}

Include the likely sales driver and one store-level recommendation.
"""
            ai_explanation = llm.invoke(prompt).content

        db.predictions.insert_one(
            {
                "input": data.model_dump(),
                "azure_prediction": azure_prediction,
                "local_prediction": local_prediction,
                "ai_explanation": ai_explanation,
            }
        )

        return {
            "azure_ml_prediction": azure_prediction,
            "local_prediction": local_prediction,
            "ai_explanation": ai_explanation,
        }

    except Exception as exc:
        logger.error(f"Prediction Error: {exc}")
        return {"error": str(exc)}


@app.post("/data-ingestion", tags=["data"])
def ingest_sales(request: SalesIngestionRequest):
    logger.info(f"POST /data-ingestion records={len(request.records)}")

    try:
        db = get_db()
        if db is None:
            raise HTTPException(status_code=503, detail="Database connection failed")

        records = [record.model_dump() for record in request.records]
        if not records:
            raise HTTPException(status_code=400, detail="No sales records provided")

        result = db.sales_data.insert_many(records)

        return {
            "inserted_count": len(result.inserted_ids),
            "status": "Sales data ingested successfully",
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Data Ingestion Error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/search-documents", tags=["search"])
def search_documents(request: DocumentSearchRequest):
    logger.info(f"POST /search-documents query={request.query!r}")

    try:
        if retriever is None:
            raise HTTPException(
                status_code=503,
                detail="Document retriever is not initialized",
            )

        documents = retriever.invoke(request.query)
        selected_docs = documents[: request.top_k]

        search_results = [
            {
                "content": doc.page_content,
                "metadata": getattr(doc, "metadata", {}),
            }
            for doc in selected_docs
        ]

        answer = None

        if qa_chain is not None:
            try:
                context = "\n\n".join(doc.page_content for doc in selected_docs)
                prompt = f"Context:\n{context}\n\nQuestion: {request.query}"
                answer = qa_chain.invoke(prompt).content
            except Exception as exc:
                logger.warning(f"QA answer generation failed: {exc}")

        return {
            "query": request.query,
            "top_k": request.top_k,
            "documents": search_results,
            "answer": answer,
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Document Search Error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/detect-anomalies", tags=["anomaly"])
def detect_anomalies():
    logger.info("GET /detect-anomalies")

    try:
        anomaly_file = os.path.join("data", "anomaly_results.csv")
        if not os.path.exists(anomaly_file):
            raise HTTPException(status_code=404, detail="Anomaly results file not found")

        df = pd.read_csv(anomaly_file)
        anomaly_counts = df["anomaly"].value_counts().to_dict()
        anomaly_records = df[df["anomaly"] == "Anomaly"].head(10)

        return {
            "total_anomalies": int(anomaly_counts.get("Anomaly", 0)),
            "totals": anomaly_counts,
            "sample_anomalies": anomaly_records.to_dict(orient="records"),
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Anomaly Detection Error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/multi-agent")
def multi_agent_system(request: AgentRequest):
    logger.info(f"POST /multi-agent question={request.question!r}")

    try:
        route_result = route_query(request.question)

        return {
            "question": request.question,
            "agent_used": route_result.get("agent"),
            "agent_type": route_result.get("agent_type"),
            "response": route_result.get("response"),
            "status": "success",
        }

    except Exception as exc:
        logger.error(f"Multi-Agent Error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/ask", tags=["qa"])
def ask_question(request: AgentRequest):
    logger.info(f"POST /ask question={request.question!r}")

    try:
        db = get_db()
        if db is None:
            raise HTTPException(status_code=500, detail="Database unavailable")

        if llm is None:
            raise HTTPException(status_code=500, detail="LLM not configured")

        response = llm.invoke(request.question)

        try:
            db.qa_logs.insert_one(
                {
                    "question": request.question,
                    "response": response.content,
                    "endpoint": "/ask",
                    "timestamp": pd.Timestamp.now(),
                }
            )
        except Exception as exc:
            logger.warning(f"Failed to log Q&A: {exc}")

        return {
            "question": request.question,
            "answer": response.content,
            "type": "direct_qa",
            "status": "success",
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Q&A Error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/sales-data", tags=["data"])
def get_sales_data(limit: int = 10):
    logger.info(f"GET /sales-data limit={limit}")

    try:
        db = get_db()
        if db is None:
            raise HTTPException(status_code=500, detail="Database unavailable")

        data = list(db.sales_data.find().limit(limit))

        for record in data:
            if "_id" in record:
                record["_id"] = str(record["_id"])

        return {
            "status": "success",
            "data": data,
            "count": len(data),
        }

    except Exception as exc:
        logger.error(f"Sales Data Error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/document-intelligence", tags=["document-intelligence"])
async def extract_document(file: UploadFile = File(...)):
    logger.info(f"POST /document-intelligence filename={file.filename}")

    try:
        if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Only PDF and image files allowed")

        file_path = os.path.join(UPLOAD_DIR, file.filename)
        content = await file.read()

        with open(file_path, "wb") as saved_file:
            saved_file.write(content)

        if not doc_intel_client:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Document Intelligence is not configured. Set "
                    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and "
                    "AZURE_DOCUMENT_INTELLIGENCE_API_KEY."
                ),
            )

        with open(file_path, "rb") as source_file:
            poller = doc_intel_client.begin_analyze_document(
                "prebuilt-layout",
                body=source_file,
            )

        result = poller.result()

        return {
            "status": "success",
            "filename": file.filename,
            "pages": len(result.pages) if hasattr(result, "pages") else 0,
            "content": result.content if hasattr(result, "content") else "",
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Document Intelligence Error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
