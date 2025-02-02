import random
import time
import logging
from typing import Dict, List, Any, Tuple

from bson import ObjectId
from pymongo.synchronous.database import Database

from mongo.connection_info import mongo_dsl, get_mongo_db

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def measure_user_favorites(db: Database, user_id: ObjectId) -> float:
    start_time = time.perf_counter()
    list(db.favorites.find({"user_id": user_id}, {"movie_id": 1, "_id": 0}))
    end_time = time.perf_counter()
    return end_time - start_time


def measure_movie_average_rating(db: Database, movie_id: ObjectId) -> float:
    start_time = time.perf_counter()
    pipeline: List[Dict[str, Any]] = [
        {"$match": {"movie_id": movie_id}},
        {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}}}
    ]
    list(db.ratings.aggregate(pipeline))
    end_time = time.perf_counter()
    return end_time - start_time


def measure_scenario(
    db: Database,
    ids: List[ObjectId],
    measure_func,
    iterations: int
) -> Tuple[float, float]:
    times = [
        measure_func(db, obj_id)
        for obj_id in random.choices(ids, k=iterations)
    ]
    total_time = sum(times)
    avg_time = total_time / iterations
    return total_time, avg_time


def test_queries(dsl: Dict, iterations: int = 100) -> None:
    db = get_mongo_db(dsl)

    user_ids = [doc["_id"] for doc in db.users.find({}, {"_id": 1})]
    movie_ids = [doc["_id"] for doc in db.movies.find({}, {"_id": 1})]

    if not user_ids:
        raise ValueError("No users found")
    if not movie_ids:
        raise ValueError("No movies found")

    total_time_fav, avg_time_fav = measure_scenario(
        db,
        user_ids,
        measure_user_favorites,
        iterations
    )
    total_time_rating, avg_time_rating = measure_scenario(
        db,
        movie_ids,
        measure_movie_average_rating,
        iterations
    )

    logging.info("Сценарий «список закладок»:")
    logging.info(
        "  Общее время для %s итераций: %s",
        iterations,
        total_time_fav
    )
    logging.info(
        "  Среднее время на один запрос: %s",
        avg_time_fav
    )

    logging.info("Сценарий «средняя оценка фильма»:")
    logging.info(
        "  Общее время для %s итераций: %s",
        iterations,
        total_time_rating
    )
    logging.info(
        "  Среднее время на один запрос: %s",
        avg_time_rating
    )


if __name__ == "__main__":
    test_queries(mongo_dsl)
