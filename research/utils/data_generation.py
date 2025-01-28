from enum import Enum
from typing import List, Tuple
from uuid import UUID

from bson import ObjectId
from faker import Faker
import uuid
import random


class IDType(Enum):
    ObjectId = 0,
    UUID = 1


ID = uuid.UUID | ObjectId


def generate_id(id_type: IDType) -> ID:
    if id_type == IDType.ObjectId:
        return ObjectId()
    elif id_type == IDType.UUID:
        return uuid.uuid4()
    else:
        raise ValueError(f'Unexpected type {id_type}')


def get_unique_pair_(
        user_data: List,
        movie_data: List,
        data_len: int
) -> List[Tuple[ID, ID]]:
    all_pairs = [
        (user['id'], movie['id'])
        for user in user_data
        for movie in movie_data
    ]

    max_pairs = len(all_pairs)
    if data_len > max_pairs:
        raise ValueError("Max pairs reached")

    random.shuffle(all_pairs)

    return all_pairs[:data_len]


def get_unique_pair(user_data, movie_data, data_len):
    """
    Возвращает data_len уникальных пар (user_id, movie_id),
    не создавая весь список пар и не делая shuffle.
    """
    n = len(user_data)
    m = len(movie_data)
    max_pairs = n * m
    if data_len > max_pairs:
        raise ValueError("Max pairs reached")

    # 1. Выбираем случайные уникальные индексы из диапазона [0 .. n*m-1]
    indices = random.sample(range(max_pairs), data_len)

    # 2. Преобразуем индекс -> (user_idx, movie_idx)
    #    user_idx = idx // m, movie_idx = idx % m
    result = []
    for idx in indices:
        user_idx = idx // m
        movie_idx = idx % m
        result.append((user_data[user_idx]['id'], movie_data[movie_idx]['id']))

    return result


def generate_data(
        id_type: IDType,
        user_len: int = 10000,
        movie_len: int = 10000,
        rating_len: int = 10000,
        favorite_len: int = 10000,
        review_len: int = 10000,
        review_likes_len: int = 10000,
):
    fake = Faker()

    def get_id() -> UUID | ObjectId:
        return generate_id(id_type)

    user_data = []
    for _ in range(user_len):
        user_data.append({
            'id': get_id(),
            'login': fake.user_name(),
            'password_hash': fake.sha256(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name()
        })

    movie_data = []
    for _ in range(movie_len):
        movie_data.append({
            'id': get_id(),
            'title': fake.sentence(nb_words=3),
            'description': fake.text(max_nb_chars=50),
            'creation_date': fake.date_this_decade(),
            'rating': round(random.uniform(0, 10), 1),
            'type': random.choice(['movie', 'series', 'cartoon'])
        })

    rating_data = []
    unique_pairs = get_unique_pair(user_data, movie_data, rating_len)
    for user_id, movie_id in unique_pairs:
        rating_data.append(
            {
                'user_id': user_id,
                'movie_id': movie_id,
                'rating': random.randint(0, 10)
            }
        )

    favorite_data = []
    unique_pairs = get_unique_pair(user_data, movie_data, favorite_len)
    for user_id, movie_id in unique_pairs:
        favorite_data.append(
            {
                'user_id': user_id,
                'movie_id': movie_id
            }
        )

    review_data = []
    for _ in range(review_len):
        review_data.append({
            'id': get_id(),
            'user_id': random.choice(user_data)['id'],
            'movie_id': random.choice(movie_data)['id'],
            'review_text': fake.paragraph(nb_sentences=3)
        })

    review_likes_data = []
    unique_pairs = get_unique_pair(user_data, review_data, review_likes_len)
    for user_id, movie_id in unique_pairs:
        review_likes_data.append(
            {
                'id': get_id(),
                'user_id': user_id,
                'review_id': movie_id,
                'is_like': bool(random.getrandbits(1))
            }
        )

    return {
        "user_data": user_data,
        "movie_data": movie_data,
        "rating_data": rating_data,
        "favorite_data": favorite_data,
        "review_data": review_data,
        "review_likes_data": review_likes_data
    }


if __name__ == '__main__':
    data = generate_data(
        IDType.ObjectId,
        10,
        10,
        10,
        10,
        10,
        10
    )

    print(data)
