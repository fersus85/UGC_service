import os
from typing import Dict

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.synchronous.database import Database

load_dotenv()

mongo_dsl = {
    "dbname": os.getenv("MONGO_DBNAME", "moviesDB"),
    "mongo_uri": os.getenv("MONGO_URI", "mongodb://localhost:27017/"),
}


def get_mongo_db(dsl: Dict) -> Database:
    mongo_uri = dsl.get("mongo_uri")
    client: MongoClient = MongoClient(mongo_uri)

    return client[dsl.get("database", "moviesDB")]
