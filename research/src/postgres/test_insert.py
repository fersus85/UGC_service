import time
import logging
from typing import List, Dict, Callable, Any

import psycopg
from helpers.data_generation import generate_data, IDType
from postgres.connection_info import pg_dsl

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def prepare_users_movies(user_data: List[Dict], movie_data: List[Dict], dsl: Dict) -> None:
    batch_size = 5000
    with psycopg.connect(**dsl) as conn:
        with conn.cursor() as cur:
            # Вставка пользователей
            for start_idx in range(0, len(user_data), batch_size):
                batch = user_data[start_idx:start_idx + batch_size]
                if not batch:
                    continue
                users_to_insert = [
                    (
                        row['id'],
                        row['login'],
                        row['password_hash'],
                        row.get('first_name'),
                        row.get('last_name')
                    )
                    for row in batch
                ]
                sql_users = """
                    INSERT INTO users (
                        id,
                        login,
                        password_hash,
                        first_name,
                        last_name
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """
                cur.executemany(sql_users, users_to_insert)
            # Вставка фильмов
            for start_idx in range(0, len(movie_data), batch_size):
                batch = movie_data[start_idx:start_idx + batch_size]
                if not batch:
                    continue
                movies_to_insert = [
                    (
                        row['id'],
                        row['title'],
                        row.get('description'),
                        row.get('creation_date'),
                        row.get('rating'),
                        row.get('type')
                    )
                    for row in batch
                ]
                sql_movies = """
                    INSERT INTO movies (
                        id, title, description, creation_date, rating, type
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cur.executemany(sql_movies, movies_to_insert)
            conn.commit()


def batch_insert(
    cur,
    data: List[Dict],
    sql: str,
    transform: Callable[[Dict], Any],
    batch_size: int
) -> float:
    total_time = float(0)
    for start_idx in range(0, len(data), batch_size):
        batch = data[start_idx:start_idx + batch_size]
        if not batch:
            continue
        values = [transform(row) for row in batch]
        start_time = time.perf_counter()
        cur.executemany(sql, values)
        total_time += time.perf_counter() - start_time
    return total_time


def insert_data(data: Dict[str, List[Dict]], dsl: Dict, batch_size: int = 5000) -> None:
    prepare_users_movies(data['user_data'], data['movie_data'], dsl)
    total_insertion_time = float(0)

    tasks = [
        (
            "ratings",
            "INSERT INTO ratings (user_id, movie_id, rating) VALUES (%s, %s, %s)",
            data["rating_data"],
            lambda row: (row["user_id"], row["movie_id"], row["rating"])
        ),
        (
            "favorites",
            "INSERT INTO favorites (user_id, movie_id) VALUES (%s, %s)",
            data["favorite_data"],
            lambda row: (row["user_id"], row["movie_id"])
        ),
        (
            "reviews",
            "INSERT INTO reviews (id, user_id, movie_id, review_text) VALUES (%s, %s, %s, %s)",
            data["review_data"],
            lambda row: (row["id"], row["user_id"], row["movie_id"], row["review_text"])
        ),
        (
            "review_likes",
            "INSERT INTO review_likes (id, review_id, user_id, is_like) VALUES (%s, %s, %s, %s)",
            data["review_likes_data"],
            lambda row: (row["id"], row["review_id"], row["user_id"], row["is_like"])
        )
    ]

    with psycopg.connect(**dsl) as conn:
        with conn.cursor() as cur:
            for table_name, sql, task_data, transform in tasks:
                task_time = batch_insert(cur, task_data, sql, transform, batch_size)
                logging.info("Вставка в %s заняла: %s", table_name, task_time)
                total_insertion_time += task_time
            conn.commit()

    logging.info("Общее время отправки данных во все таблицы: %s", total_insertion_time)


if __name__ == "__main__":
    generated_data = generate_data(IDType.UUID)
    insert_data(generated_data, pg_dsl)
