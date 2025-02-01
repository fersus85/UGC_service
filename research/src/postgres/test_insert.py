import time
import logging
from typing import List, Dict, Callable, Any

import psycopg
from utils.data_generation import generate_data, IDType
from postgres.connection_info import pg_dsl

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def prepare_users_movies(user_data: List[Dict], movie_data: List[Dict], dsl: Dict) -> None:
    batch_size = 5000
    with psycopg.connect(**dsl) as conn:
        with conn.cursor() as cur:
            # Вставка пользователей
            for start_idx in range(0, len(user_data), batch_size):
                end_idx = start_idx + batch_size
                batch = user_data[start_idx:end_idx]
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
                end_idx = start_idx + batch_size
                batch = movie_data[start_idx:end_idx]
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
        end_idx = start_idx + batch_size
        batch = data[start_idx:end_idx]
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
    with psycopg.connect(**dsl) as conn:
        with conn.cursor() as cur:
            # Вставка оценок (ratings)
            sql_ratings = "INSERT INTO ratings (user_id, movie_id, rating) VALUES (%s, %s, %s)"
            time_ratings = batch_insert(
                cur,
                data['rating_data'],
                sql_ratings,
                lambda row: (row['user_id'], row['movie_id'], row['rating']),
                batch_size
            )
            logging.info("Вставка в ratings заняла: %s", time_ratings)
            total_insertion_time += time_ratings

            # Вставка избранного (favorites)
            sql_favorites = "INSERT INTO favorites (user_id, movie_id) VALUES (%s, %s)"
            time_favorites = batch_insert(
                cur,
                data['favorite_data'],
                sql_favorites,
                lambda row: (row['user_id'], row['movie_id']),
                batch_size
            )
            logging.info("Вставка в favorites заняла: %s", time_favorites)
            total_insertion_time += time_favorites

            # Вставка отзывов (reviews)
            sql_reviews = "INSERT INTO reviews (id, user_id, movie_id, review_text) VALUES (%s, %s, %s, %s)"
            time_reviews = batch_insert(
                cur,
                data['review_data'],
                sql_reviews,
                lambda row: (row['id'], row['user_id'], row['movie_id'], row['review_text']),
                batch_size
            )
            logging.info("Вставка в reviews заняла: %s", time_reviews)
            total_insertion_time += time_reviews

            # Вставка лайков к отзывам (review_likes)
            sql_review_likes = "INSERT INTO review_likes (id, review_id, user_id, is_like) VALUES (%s, %s, %s, %s)"
            time_review_likes = batch_insert(
                cur,
                data['review_likes_data'],
                sql_review_likes,
                lambda row: (row['id'], row['review_id'], row['user_id'], row['is_like']),
                batch_size
            )
            logging.info("Вставка в review_likes заняла: %s", time_review_likes)
            total_insertion_time += time_review_likes

            conn.commit()
    logging.info("Общее время отправки данных во все таблицы: %s", total_insertion_time)


if __name__ == "__main__":
    generated_data = generate_data(IDType.UUID)
    insert_data(generated_data, pg_dsl)
