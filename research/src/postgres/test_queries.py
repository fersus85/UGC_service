import random
import time
import logging
from typing import Dict

import psycopg
from postgres.connection_info import pg_dsl

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def measure_user_favorites(conn: psycopg.Connection, user_id: str) -> float:
    start_time = time.perf_counter()
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT movie_id FROM favorites WHERE user_id = '{user_id}'"
        )
        cur.fetchall()
    end_time = time.perf_counter()
    return end_time - start_time


def measure_movie_average_rating(conn: psycopg.Connection, movie_id: str) -> float:
    start_time = time.perf_counter()
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT AVG(rating) FROM ratings WHERE movie_id = '{movie_id}'"
        )
        cur.fetchone()
    end_time = time.perf_counter()
    return end_time - start_time


def test_queries(dsl: Dict, iterations: int = 100) -> None:
    with psycopg.connect(**dsl) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users")
            all_user_ids = [row[0] for row in cur.fetchall()]

            cur.execute("SELECT id FROM movies")
            all_movie_ids = [row[0] for row in cur.fetchall()]

        if not all_user_ids:
            raise ValueError("No users found")
        if not all_movie_ids:
            raise ValueError("No movies found")

        random_user_ids = random.choices(all_user_ids, k=iterations)
        random_movie_ids = random.choices(all_movie_ids, k=iterations)

        total_time_fav = sum(measure_user_favorites(conn, user_id) for user_id in random_user_ids)
        avg_time_fav = total_time_fav / iterations

        total_time_rating = sum(measure_movie_average_rating(conn, movie_id) for movie_id in random_movie_ids)
        avg_time_rating = total_time_rating / iterations

        logging.info("Сценарий «список закладок»:")
        logging.info("  Общее время: %s", total_time_fav)
        logging.info("  Среднее время на один запрос: %s", avg_time_fav)

        logging.info("Сценарий «средняя оценка фильма»:")
        logging.info("  Общее время: %s", total_time_rating)
        logging.info("  Среднее время на один запрос: %s", avg_time_rating)


if __name__ == "__main__":
    test_queries(pg_dsl)
