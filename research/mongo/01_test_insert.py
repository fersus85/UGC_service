import datetime
import time
from typing import List, Dict

from mongo.connection_info import dsl, get_mongo_db
from utils.data_generation import generate_data, IDType


def insert_data(
        user_data: List[Dict],
        movie_data: List[Dict],
        rating_data: List[Dict],
        favorite_data: List[Dict],
        review_data: List[Dict],
        review_likes_data: List[Dict],
        dsl: Dict,
        batch_size: int = 5000
) -> None:
    db = get_mongo_db(dsl)

    def batch_insert(
            collection_name: str,
            documents: List[Dict],
            transform_func=None
    ) -> None:
        collection = db[collection_name]
        total_docs = len(documents)

        insertion_time = 0.0
        for i in range(0, total_docs, batch_size):
            chunk = documents[i: i + batch_size]
            if transform_func:
                for doc in chunk:
                    transform_func(doc)

            start_send = time.perf_counter()
            collection.insert_many(chunk, ordered=False)
            end_send = time.perf_counter()

            insertion_time += (end_send - start_send)

        print(f"Вставка в {collection_name} заняла: {insertion_time}")

    def transform_user(doc: Dict) -> None:
        if "id" in doc:
            doc["_id"] = doc.pop("id")

        if "created_at" not in doc:
            doc["created_at"] = datetime.datetime.now(datetime.UTC)

    def transform_movie(doc: Dict) -> None:
        if "id" in doc:
            doc["_id"] = doc.pop("id")

        if isinstance(doc.get("creation_date"), datetime.date):
            doc["creation_date"] = datetime.datetime.combine(
                doc["creation_date"], datetime.time.min
            )

        if "created" not in doc:
            doc["created"] = datetime.datetime.now(datetime.UTC)
        if "modified" not in doc:
            doc["modified"] = doc["created"]

    def transform_rating(doc: Dict):
        if "created_at" not in doc:
            doc["created_at"] = datetime.datetime.now(datetime.UTC)

    def transform_favorite(doc: Dict):
        if "created_at" not in doc:
            doc["created_at"] = datetime.datetime.now(datetime.UTC)

    def transform_review(doc: Dict):
        if "id" in doc:
            doc["_id"] = doc.pop("id")

        if "created_at" not in doc:
            doc["created_at"] = datetime.datetime.now(datetime.UTC)

    def transform_review_like(doc: Dict):
        if "id" in doc:
            doc["_id"] = doc.pop("id")

        if "created_at" not in doc:
            doc["created_at"] = datetime.datetime.now(datetime.UTC)

    to_insert = [
        ("users", user_data, transform_user),
        ("movies", movie_data, transform_movie),
        ("ratings", rating_data, transform_rating),
        ("favorites", favorite_data, transform_favorite),
        ("reviews", review_data, transform_review),
        ("review_likes", review_likes_data, transform_review_like),
    ]

    for collection_name, documents, transform_func in to_insert:
        batch_insert(collection_name, documents, transform_func)


if __name__ == "__main__":
    data = generate_data(
        IDType.ObjectId,
    )

    insert_data(
        **data,
        dsl=dsl
    )
