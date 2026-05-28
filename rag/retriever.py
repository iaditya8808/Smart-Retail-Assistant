import os
import sys
import warnings
import logging
from io import StringIO

# Disable ChromaDB telemetry before importing
os.environ["ANONYMIZED_TELEMETRY"] = "False"

os.environ["CHROMA_TELEMETRY_IMPL"] = "none"

# Suppress specific ChromaDB stderr warnings
class SuppressChromaDBWarnings(logging.Filter):
    def filter(self, record):
        if "capture()" in record.getMessage():
            return False
        return True

# Apply filter to root logger
logging.getLogger().addFilter(SuppressChromaDBWarnings())

# Suppress ChromaDB telemetry warnings at the warnings level
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
from langchain_chroma import Chroma

from rag.embeddings import get_azure_embeddings

load_dotenv()

vectorstore = Chroma(
    persist_directory="rag/chroma_db",
    embedding_function=get_azure_embeddings(),
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

print("ChromaDB retriever loaded")
