import os

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings


load_dotenv()

DATA_PATH = "../data"
PERSIST_DIR = "chroma_db"

documents = []

for file_name in os.listdir(DATA_PATH):
    if not file_name.endswith(".pdf"):
        continue

    pdf_path = os.path.join(DATA_PATH, file_name)
    print(f"Loading PDF: {file_name}")

    loader = PyPDFLoader(pdf_path)
    documents.extend(loader.load())

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

docs = text_splitter.split_documents(documents)
print(f"Document chunks created: {len(docs)}")

embeddings_deployment = (
    os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    or os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT")
)

if not embeddings_deployment:
    raise ValueError("Set AZURE_OPENAI_EMBEDDING_DEPLOYMENT in .env")

embeddings = AzureOpenAIEmbeddings(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=embeddings_deployment,
    model="text-embedding-ada-002",
)

embeddings.embed_query("test")
print(f"Azure OpenAI embeddings ready: {embeddings_deployment}")

Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory=PERSIST_DIR,
)

print(f"Vector store written to {PERSIST_DIR}")
