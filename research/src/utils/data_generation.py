# flake8: noqa: WPS202
from enum import Enum
from typing import List, Tuple, Dict, Callable
from uuid import UUID, uuid4

from bson import ObjectId
from faker import Faker
import random

ID = UUID | ObjectId


class IDType(Enum):
    ObjectId = 0
    UUID = 1


def generate_id(id_type: IDType) -> ID:
    if id_type == IDType.ObjectId:
        return ObjectId()
    elif id_type == IDType.UUID:
        return uuid4()
    else:
        raise ValueError(f"Unexpected type {id_type}")


def get_unique_pair(
        user_data: List[Dict],
        movie_data: List[Dict],
        data_len: int
) -> List[Tuple[ID, ID]]:
    num_users = len(user_data)
    num_movies = len(movie_data)
    max_pairs = num_users * num_movies
    if data_len > max_pairs:
        raise ValueError("Max pairs reached")
    indices = random.sample(range(max_pairs), data_len)
    result = []
    for idx in indices:
        user_idx = idx // num_movies
        movie_idx = idx % num_movies
        result.append((user_data[user_idx]['id'], movie_data[movie_idx]['id']))
    return result


def generate_users(
        fake: Faker, get_id: Callable[[], ID], user_len: int
) -> List[Dict]:
    return [{
        'id': get_id(),
        'login': fake.user_name(),
        'password_hash': fake.sha256(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name()
    } for _ in range(user_len)]


def generate_movies(
        fake: Faker, get_id: Callable[[], ID], movie_len: int
) -> List[Dict]:
    return [{
        'id': get_id(),
        'title': fake.sentence(nb_words=3),
        'description': fake.text(max_nb_chars=50),
        'creation_date': fake.date_this_decade(),
        'rating': round(random.uniform(0, 10), 1),
        'type': random.choice(['movie', 'series', 'cartoon'])
    } for _ in range(movie_len)]


def generate_ratings(
        user_data: List[Dict], movie_data: List[Dict], rating_len: int
) -> List[Dict]:
    pairs = get_unique_pair(user_data, movie_data, rating_len)
    return [{
        'user_id': user_id,
        'movie_id': movie_id,
        'rating': random.randint(0, 10)
    } for user_id, movie_id in pairs]


def generate_favorites(
        user_data: List[Dict], movie_data: List[Dict], favorite_len: int
) -> List[Dict]:
    pairs = get_unique_pair(user_data, movie_data, favorite_len)
    return [{
        'user_id': user_id,
        'movie_id': movie_id
    } for user_id, movie_id in pairs]


def generate_reviews(
        fake: Faker,
        get_id: Callable[[], ID],
        user_data: List[Dict],
        movie_data: List[Dict],
        review_len: int
) -> List[Dict]:
    return [{
        'id': get_id(),
        'user_id': random.choice(user_data)['id'],
        'movie_id': random.choice(movie_data)['id'],
        'review_text': fake.paragraph(nb_sentences=3)
    } for _ in range(review_len)]


def generate_review_likes(
        get_id: Callable[[], ID],
        user_data: List[Dict],
        review_data: List[Dict],
        review_likes_len: int
) -> List[Dict]:
    pairs = get_unique_pair(user_data, review_data, review_likes_len)
    return [{
        'id': get_id(),
        'user_id': user_id,
        'review_id': review_id,
        'is_like': bool(random.getrandbits(1))
    } for user_id, review_id in pairs]


def generate_data(
        id_type: IDType,
        lengths: Dict[str, int] | None = None
) -> Dict[str, List[Dict]]:
    """
    Генерирует тестовые данные.

    Параметр lengths – словарь, содержащий размеры для:
        "user_len", "movie_len", "rating_len",
        "favorite_len", "review_len", "review_likes_len"
    Если lengths не передан, используются значения по умолчанию.
    """
    if lengths is None:
        lengths = {
            "user_len": 100_000,
            "movie_len": 100_000,
            "rating_len": 1_000_000,
            "favorite_len": 1_000_000,
            "review_len": 1_000_000,
            "review_likes_len": 1_000_000,
        }
    fake = Faker()
    get_id = lambda: generate_id(id_type)
    users = generate_users(fake, get_id, lengths["user_len"])
    movies = generate_movies(fake, get_id, lengths["movie_len"])
    ratings = generate_ratings(users, movies, lengths["rating_len"])
    favorites = generate_favorites(users, movies, lengths["favorite_len"])
    reviews = generate_reviews(
        fake, get_id, users, movies,lengths["review_len"]
    )
    review_likes = generate_review_likes(
        get_id, users, reviews, lengths["review_likes_len"]
    )
    return {
        "user_data": users,
        "movie_data": movies,
        "rating_data": ratings,
        "favorite_data": favorites,
        "review_data": reviews,
        "review_likes_data": review_likes
    }


if __name__ == '__main__':
    import logging

    logging.basicConfig(
        level=logging.INFO,format="%(levelname)s: %(message)s"
    )
    data = generate_data(
        IDType.ObjectId,
        {
            "user_len": 10,
            "movie_len": 10,
            "rating_len": 10,
            "favorite_len": 10,
            "review_len": 10,
            "review_likes_len": 10,
        }
    )
    logging.info(data)
