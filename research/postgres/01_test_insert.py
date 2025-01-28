import time
from typing import List, Dict

import psycopg

from postgres.connection_info import dsl
from utils.data_generation import generate_data, IDType


def prepare_users_movies(
        user_data: List[Dict],
        movie_data: List[Dict],
        dsl: Dict
) -> None:
    batch_size = 5000

    with psycopg.connect(**dsl) as conn:
        with conn.cursor() as cur:

            # USERS
            for i in range(0, len(user_data), batch_size):
                chunk = user_data[i:i + batch_size]
                if not chunk:
                    continue

                users_to_insert = [
                    (
                        row['id'],
                        row['login'],
                        row['password_hash'],
                        row.get('first_name'),
                        row.get('last_name')
                    )
                    for row in chunk
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

            # MOVIES
            for i in range(0, len(movie_data), batch_size):
                chunk = movie_data[i:i + batch_size]
                if not chunk:
                    continue

                movies_to_insert = [
                    (
                        row['id'],
                        row['title'],
                        row.get('description'),
                        row.get('creation_date'),
                        row.get('rating'),
                        row.get('type'),
                    )
                    for row in chunk
                ]

                sql_movies = """
                    INSERT INTO movies (
                        id, title, description, creation_date, rating, type
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                """

                cur.executemany(sql_movies, movies_to_insert)


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
    prepare_users_movies(user_data, movie_data, dsl)

    # Общий счётчик времени вставки (только отправка в БД)
    total_insertion_time = 0.0

    with psycopg.connect(**dsl) as conn:
        with conn.cursor() as cur:
            # RATINGS
            insertion_time_ratings = 0.0
            for i in range(0, len(rating_data), batch_size):
                chunk = rating_data[i:i + batch_size]
                if not chunk:
                    continue

                ratings_to_insert = [
                    (
                        row['user_id'],
                        row['movie_id'],
                        row['rating'],
                    )
                    for row in chunk
                ]

                sql_ratings = """
                    INSERT INTO ratings (user_id, movie_id, rating)
                    VALUES (%s, %s, %s)
                """

                start_send = time.perf_counter()
                cur.executemany(sql_ratings, ratings_to_insert)
                end_send = time.perf_counter()

                insertion_time_ratings += (end_send - start_send)

            print(f"Вставка в ratings заняла: {insertion_time_ratings}")
            total_insertion_time += insertion_time_ratings

            # FAVORITES
            insertion_time_favorites = 0.0
            for i in range(0, len(favorite_data), batch_size):
                chunk = favorite_data[i: i + batch_size]
                if not chunk:
                    continue

                favorites_to_insert = [
                    (
                        row['user_id'],
                        row['movie_id'],
                    )
                    for row in chunk
                ]

                sql_favorites = """
                    INSERT INTO favorites (user_id, movie_id)
                    VALUES (%s, %s)
                """

                start_send = time.perf_counter()
                cur.executemany(sql_favorites, favorites_to_insert)
                end_send = time.perf_counter()

                insertion_time_favorites += (end_send - start_send)

            print(f"Вставка в favorites заняла: {insertion_time_favorites}")
            total_insertion_time += insertion_time_favorites

            # REVIEWS
            insertion_time_reviews = 0.0
            for i in range(0, len(review_data), batch_size):
                chunk = review_data[i:i + batch_size]
                if not chunk:
                    continue

                reviews_to_insert = [
                    (
                        row['id'],
                        row['user_id'],
                        row['movie_id'],
                        row['review_text'],
                    )
                    for row in chunk
                ]

                sql_reviews = """
                    INSERT INTO reviews (id, user_id, movie_id, review_text)
                    VALUES (%s, %s, %s, %s)
                """

                start_send = time.perf_counter()
                cur.executemany(sql_reviews, reviews_to_insert)
                end_send = time.perf_counter()

                insertion_time_reviews += (end_send - start_send)

            print(f"Вставка в reviews заняла: {insertion_time_reviews}")
            total_insertion_time += insertion_time_reviews

            # REVIEW_LIKES
            insertion_time_review_likes = 0.0
            for i in range(0, len(review_likes_data), batch_size):
                chunk = review_likes_data[i:i + batch_size]
                if not chunk:
                    continue

                review_likes_to_insert = [
                    (
                        row['id'],
                        row['review_id'],
                        row['user_id'],
                        row['is_like'],
                    )
                    for row in chunk
                ]

                sql_review_likes = """
                    INSERT INTO review_likes (id, review_id, user_id, is_like)
                    VALUES (%s, %s, %s, %s)
                """

                start_send = time.perf_counter()
                cur.executemany(sql_review_likes, review_likes_to_insert)
                end_send = time.perf_counter()

                insertion_time_review_likes += (end_send - start_send)

            print(
                f"Вставка в review_likes заняла: {insertion_time_review_likes}"
            )
            total_insertion_time += insertion_time_review_likes

            conn.commit()

    print(
        "Общее чистое время отправки"
        f" данных во все таблицы: {total_insertion_time}"
    )


def insert_data_(
        user_data: List[Dict],
        movie_data: List[Dict],
        rating_data: List[Dict],
        favorite_data: List[Dict],
        review_data: List[Dict],
        review_likes_data: List[Dict],
        dsl: Dict,
        batch_size: int = 5000
) -> None:
    prepare_users_movies(user_data, movie_data, dsl)

    with psycopg.connect(**dsl) as conn:
        with conn.cursor() as cur:
            # RATINGS
            for i in range(0, len(rating_data), batch_size):
                chunk = rating_data[i:i + batch_size]
                if not chunk:
                    continue

                ratings_to_insert = [
                    (
                        row['user_id'],
                        row['movie_id'],
                        row['rating'],
                    )
                    for row in chunk
                ]

                sql_ratings = """
                    INSERT INTO ratings (user_id, movie_id, rating)
                    VALUES (%s, %s, %s)
                """

                cur.executemany(sql_ratings, ratings_to_insert)

            # FAVORITES
            for i in range(0, len(favorite_data), batch_size):
                chunk = favorite_data[i:i + batch_size]
                if not chunk:
                    continue

                favorites_to_insert = [
                    (
                        row['user_id'],
                        row['movie_id'],
                    )
                    for row in chunk
                ]

                sql_favorites = """
                    INSERT INTO favorites (user_id, movie_id)
                    VALUES (%s, %s)
                """

                cur.executemany(sql_favorites, favorites_to_insert)

            # REVIEWS
            for i in range(0, len(review_data), batch_size):
                chunk = review_data[i:i + batch_size]
                if not chunk:
                    continue

                reviews_to_insert = [
                    (
                        row['id'],
                        row['user_id'],
                        row['movie_id'],
                        row['review_text'],
                    )
                    for row in chunk
                ]

                sql_reviews = """
                    INSERT INTO reviews (id, user_id, movie_id, review_text)
                    VALUES (%s, %s, %s, %s)
                """

                cur.executemany(sql_reviews, reviews_to_insert)

            # REVIEW_LIKES
            for i in range(0, len(review_likes_data), batch_size):
                chunk = review_likes_data[i:i + batch_size]
                if not chunk:
                    continue

                review_likes_to_insert = [
                    (
                        row['id'],
                        row['review_id'],
                        row['user_id'],
                        row['is_like'],
                    )
                    for row in chunk
                ]

                sql_review_likes = """
                    INSERT INTO review_likes (id, review_id, user_id, is_like)
                    VALUES (%s, %s, %s, %s)
                """

                cur.executemany(sql_review_likes, review_likes_to_insert)

            conn.commit()


if __name__ == "__main__":
    data = generate_data(IDType.UUID)
    insert_data(
        **data,
        dsl=dsl
    )
