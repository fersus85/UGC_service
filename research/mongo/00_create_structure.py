from typing import Dict

import pymongo

from mongo.connection_info import dsl, get_mongo_db


def initialize_mongo_schema(dsl: Dict[str, str]) -> None:
    db = get_mongo_db(dsl)

    # USERS
    users_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["login", "password_hash", "created_at"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                    "description": "Уникальный идентификатор пользователя"
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Время создания пользователя"
                },
                "login": {
                    "bsonType": "string",
                    "description": "Логин пользователя"
                },
                "password_hash": {
                    "bsonType": "string",
                    "description": "Хэш пароля"
                },
                "first_name": {
                    "bsonType": "string",
                    "description": "Имя пользователя"
                },
                "last_name": {
                    "bsonType": "string",
                    "description": "Фамилия пользователя"
                }
            }
        }
    }

    db.create_collection(
        name="users",
        validator=users_validator
    )

    # MOVIES
    movies_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "type", "created", "modified"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                    "description": "Уникальный идентификатор фильма"
                },
                "title": {
                    "bsonType": "string",
                    "description": "Название фильма"
                },
                "description": {
                    "bsonType": "string",
                    "description": "Описание фильма"
                },
                "creation_date": {
                    "bsonType": "date",
                    "description": "Дата создания"
                },
                "rating": {
                    "bsonType": "double",
                    "description": "Рейтинг"
                },
                "type": {
                    "bsonType": "string",
                    "description": "Тип фильма"
                },
                "created": {
                    "bsonType": "date",
                    "description": "Время добавления записи"
                },
                "modified": {
                    "bsonType": "date",
                    "description": "Время изменения записи"
                }
            }
        }
    }

    db.create_collection("movies", validator=movies_validator)
    db.movies.create_index([("title", pymongo.ASCENDING)])

    # RATINGS
    ratings_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "movie_id", "rating", "created_at"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                    "description": "Уникальный идентификатор документа"
                },
                "user_id": {
                    "bsonType": "objectId",
                    "description": "Ссылка на users._id"
                },
                "movie_id": {
                    "bsonType": "objectId",
                    "description": "Ссылка на movies._id"
                },
                "rating": {
                    "bsonType": "int",
                    "minimum": 0,
                    "maximum": 10,
                    "description": "Оценка (от 0 до 10)"
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Время выставления оценки"
                }
            }
        }
    }

    db.create_collection("ratings", validator=ratings_validator)

    db.ratings.create_index(
        [("user_id", pymongo.ASCENDING), ("movie_id", pymongo.ASCENDING)],
        unique=True
    )

    # FAVORITES
    favorites_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "movie_id", "created_at"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                    "description": "Уникальный идентификатор"
                },
                "user_id": {
                    "bsonType": "objectId",
                    "description": "Ссылка на _id пользователя"
                },
                "movie_id": {
                    "bsonType": "objectId",
                    "description": "Ссылка на _id фильма"
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Время добавления в избранное"
                }
            }
        }
    }

    db.create_collection("favorites", validator=favorites_validator)
    db.favorites.create_index(
        [("user_id", pymongo.ASCENDING), ("movie_id", pymongo.ASCENDING)],
        unique=True
    )

    # REVIEWS
    reviews_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "movie_id", "review_text", "created_at"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                    "description": "Уникальный идентификатор отзыва"
                },
                "user_id": {
                    "bsonType": "objectId",
                    "description": "Ссылка на _id пользователя"
                },
                "movie_id": {
                    "bsonType": "objectId",
                    "description": "Ссылка на _id фильма"
                },
                "review_text": {
                    "bsonType": "string",
                    "description": "Текст отзыва"
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Время создания отзыва"
                }
            }
        }
    }

    db.create_collection("reviews", validator=reviews_validator)
    db.reviews.create_index(
        [("user_id", pymongo.ASCENDING), ("movie_id", pymongo.ASCENDING)]
    )

    # REVIEW_LIKES
    review_likes_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["review_id", "user_id", "is_like", "created_at"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                    "description": "Уникальный идентификатор"
                },
                "review_id": {
                    "bsonType": "objectId",
                    "description": "Ссылка на reviews._id"
                },
                "user_id": {
                    "bsonType": "objectId",
                    "description": "Ссылка на users._id"
                },
                "is_like": {
                    "bsonType": "bool",
                    "description": "Лайк (true) или дизлайк (false)"
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Время установки лайка/дизлайка"
                }
            }
        }
    }

    db.create_collection("review_likes", validator=review_likes_validator)
    db.review_likes.create_index(
        [("review_id", pymongo.ASCENDING), ("user_id", pymongo.ASCENDING)],
        unique=True
    )


if __name__ == "__main__":
    initialize_mongo_schema(dsl)
