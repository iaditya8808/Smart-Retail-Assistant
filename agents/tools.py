from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["smart_retail_db"]

def fetch_sales_data():

    data = list(
        db.sales_data.find({}, {"_id": 0}).limit(20)
    )

    return str(data)

def fetch_predictions():

    data = list(
        db.predictions.find({}, {"_id": 0}).limit(10)
    )

    return str(data)