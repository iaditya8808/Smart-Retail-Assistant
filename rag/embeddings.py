import os

from langchain_openai import AzureOpenAIEmbeddings


def get_azure_embeddings(model: str = "text-embedding-3-small"):
    return AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        model=model,
    )
