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
