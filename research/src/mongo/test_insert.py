import datetime
import time
import logging
from typing import List, Dict, Callable, Optional

from mongo.connection_info import mongo_dsl, get_mongo_db
from helpers.data_generation import generate_data, IDType

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def batch_insert(
    db,
    collection_name: str,
    documents: List[Dict],
    batch_size: int,
    transform_func: Optional[Callable[[Dict], None]] = None,
) -> None:
    collection = db[collection_name]
    total_docs = len(documents)
    insertion_time = float(0)
    for start_index in range(0, total_docs, batch_size):
        chunk = documents[start_index: start_index + batch_size]
        if transform_func:
            for doc in chunk:
                transform_func(doc)
        start_send = time.perf_counter()
        collection.insert_many(chunk, ordered=False)
        end_send = time.perf_counter()
        insertion_time += end_send - start_send
    logging.info(f"Вставка в {collection_name} заняла: {insertion_time}")


def transform_with_id(doc: Dict) -> None:
    if "id" in doc:
        doc["_id"] = doc.pop("id")
    if "created_at" not in doc:
        doc["created_at"] = datetime.datetime.now(datetime.timezone.utc)


def transform_movie(doc: Dict) -> None:
    if "id" in doc:
        doc["_id"] = doc.pop("id")
    if isinstance(doc.get("creation_date"), datetime.date):
        doc["creation_date"] = datetime.datetime.combine(
            doc["creation_date"], datetime.time.min
        )
    if "created" not in doc:
        doc["created"] = datetime.datetime.now(datetime.timezone.utc)
    if "modified" not in doc:
        doc["modified"] = doc["created"]


def transform_timestamp(doc: Dict) -> None:
    if "created_at" not in doc:
        doc["created_at"] = datetime.datetime.now(datetime.timezone.utc)


def insert_data(
    data: Dict[str, List[Dict]],
    dsl: Dict,
    batch_size: int = 5000
) -> None:
    db = get_mongo_db(dsl)
    # Определяем, какие данные и какую функцию преобразования использовать
    to_insert = {
        "users": (data["user_data"], transform_with_id),
        "movies": (data["movie_data"], transform_movie),
        "ratings": (data["rating_data"], transform_timestamp),
        "favorites": (data["favorite_data"], transform_timestamp),
        "reviews": (data["review_data"], transform_with_id),
        "review_likes": (data["review_likes_data"], transform_with_id),
    }
    for collection_name, (documents, transform_func) in to_insert.items():
        batch_insert(
            db,
            collection_name,
            documents,
            batch_size,
            transform_func
        )


if __name__ == "__main__":
    generated_data = generate_data(IDType.ObjectId)
    insert_data(data=generated_data, dsl=mongo_dsl)
