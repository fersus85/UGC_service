import random
import time
from typing import Dict

import psycopg

from postgres.connection_info import dsl


def measure_user_favorites(
        conn: psycopg.Connection,
        user_id: str
) -> float:
    start_time = time.perf_counter()
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT movie_id FROM favorites WHERE user_id = '{user_id}'"
        )
        _ = cur.fetchall()
    end_time = time.perf_counter()
    return end_time - start_time


def measure_movie_average_rating(
        conn: psycopg.Connection,
        movie_id: str
) -> float:
    start_time = time.perf_counter()
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT AVG(rating) FROM ratings WHERE movie_id = '{movie_id}'"
        )
        _ = cur.fetchone()
    end_time = time.perf_counter()
    return end_time - start_time


def main(
        dsl: Dict,
        iterations: int = 100
) -> None:
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

        # замеры списка закладок пользователя
        total_time_fav = 0.0
        for user_id in random_user_ids:
            total_time_fav += measure_user_favorites(conn, user_id)
        avg_time_fav = total_time_fav / iterations

        # замеры средней оценки фильма
        total_time_rating = 0.0
        for movie_id in random_movie_ids:
            total_time_rating += measure_movie_average_rating(conn, movie_id)
        avg_time_rating = total_time_rating / iterations

        print("Сценарий «список закладок»:")
        print(f"  Общее время: {total_time_fav}")
        print(f"  Среднее время на один запрос: {avg_time_fav}")

        print("\nСценарий «средняя оценка фильма»:")
        print(f"  Общее время: {total_time_rating}")
        print(f"  Среднее время на один запрос: {avg_time_rating}")


if __name__ == "__main__":
    main(dsl)
