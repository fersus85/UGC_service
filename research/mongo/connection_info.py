import os
from typing import Dict

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.synchronous.database import Database

load_dotenv()

dsl = {
    "dbname": os.getenv("MONGO_DBNAME", "moviesDB"),
    "host": os.getenv("MONGO_HOST", "localhost"),
    "port": os.getenv("MONGO_PORT", "27017"),
}


def get_mongo_db(dsl: Dict) -> Database:
    host = dsl.get('host', 'localhost')
    port = dsl.get('port', '27017')

    mongo_uri = f"mongodb://{host}:{port}/"
    client: MongoClient = MongoClient(mongo_uri)

    return client[dsl.get("database", "moviesDB")]
