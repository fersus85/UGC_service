import random
import time
from typing import Dict, List, Any

from bson import ObjectId
from pymongo.synchronous.database import Database

from mongo.connection_info import dsl, get_mongo_db


def measure_user_favorites(db: Database, user_id: ObjectId) -> float:
    start_time = time.perf_counter()
    favorites_cursor = db.favorites.find(
        {"user_id": user_id}, {"movie_id": 1, "_id": 0}
    )
    _ = list(favorites_cursor)
    end_time = time.perf_counter()
    return end_time - start_time


def measure_movie_average_rating(db: Database, movie_id: ObjectId) -> float:
    start_time = time.perf_counter()
    pipeline: List[Dict[str, Any]] = [
        {"$match": {"movie_id": movie_id}},
        {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}}}
    ]
    cursor = db.ratings.aggregate(pipeline)
    _ = list(cursor)
    end_time = time.perf_counter()
    return end_time - start_time


def main(dsl: Dict, iterations: int = 100) -> None:
    db = get_mongo_db(dsl)

    user_ids = [doc["_id"] for doc in db.users.find({}, {"_id": 1})]
    movie_ids = [doc["_id"] for doc in db.movies.find({}, {"_id": 1})]

    if not user_ids:
        raise ValueError("No users found")
    if not movie_ids:
        raise ValueError("No movies found")

    random_user_ids = random.choices(user_ids, k=iterations)
    random_movie_ids = random.choices(movie_ids, k=iterations)

    # замеры списка закладок пользователя
    total_time_fav = 0.0
    for uid in random_user_ids:
        total_time_fav += measure_user_favorites(db, uid)
    avg_time_fav = total_time_fav / iterations

    # замеры средней оценки фильма
    total_time_rating = 0.0
    for mid in random_movie_ids:
        total_time_rating += measure_movie_average_rating(db, mid)
    avg_time_rating = total_time_rating / iterations

    print("Сценарий «список закладок»:")
    print(f"  Общее время: {total_time_fav}")
    print(f"  Среднее время на один запрос: {avg_time_fav}")

    print("\nСценарий «средняя оценка фильма»:")
    print(f"  Общее время: {total_time_rating}")
    print(f"  Среднее время на один запрос: {avg_time_rating}")


if __name__ == "__main__":
    main(dsl)
