import os
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "smart_retail_db")

# Validate Azure Configuration
azure_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "").strip()

AZURE_CONFIGURED = (
    azure_key and azure_key != "your_api_key" and
    azure_endpoint and azure_endpoint != "https://your-resource-name.openai.azure.com/" and
    azure_deployment and azure_deployment != "retail-gpt"
)

if not AZURE_CONFIGURED:
    import logging
    logging.warning(
        "Azure OpenAI not properly configured. Please update your .env file with valid credentials."
    )
