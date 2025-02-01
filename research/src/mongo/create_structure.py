# flake8: noqa: WPS202
import logging
from typing import Dict

import pymongo
from pymongo.errors import CollectionInvalid, OperationFailure
from pymongo.database import Database

from mongo.connection_info import mongo_dsl, get_mongo_db

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def enable_sharding(client: pymongo.MongoClient, db_name: str) -> None:
    try:
        client.admin.command("enableSharding", db_name)
    except OperationFailure as exc:
        logging.error("Ошибка при включении шардирования для %s: %s", db_name, exc)


def init_users(db: Database, client: pymongo.MongoClient) -> None:
    users_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["login", "password_hash", "created_at"],
            "properties": {
                "_id": {"bsonType": "objectId", "description": "Уникальный идентификатор пользователя"},
                "created_at": {"bsonType": "date", "description": "Время создания пользователя"},
                "login": {"bsonType": "string", "description": "Логин пользователя"},
                "password_hash": {"bsonType": "string", "description": "Хэш пароля"},
                "first_name": {"bsonType": "string", "description": "Имя пользователя"},
                "last_name": {"bsonType": "string", "description": "Фамилия пользователя"},
            },
        }
    }
    try:
        db.create_collection(name="users", validator=users_validator)
    except CollectionInvalid:
        logging.info("Коллекция 'users' уже существует")

    try:
        client.admin.command("shardCollection", f"{db.name}.users", key={"_id": "hashed"})
    except OperationFailure as exc:
        logging.error("Ошибка шардирования коллекции 'users': %s", exc)


def init_movies(db: pymongo.database.Database, client: pymongo.MongoClient) -> None:
    movies_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "type", "created", "modified"],
            "properties": {
                "_id": {"bsonType": "objectId", "description": "Уникальный идентификатор фильма"},
                "title": {"bsonType": "string", "description": "Название фильма"},
                "description": {"bsonType": "string", "description": "Описание фильма"},
                "creation_date": {"bsonType": "date", "description": "Дата создания"},
                "rating": {"bsonType": "double", "description": "Рейтинг"},
                "type": {"bsonType": "string", "description": "Тип фильма"},
                "created": {"bsonType": "date", "description": "Время добавления записи"},
                "modified": {"bsonType": "date", "description": "Время изменения записи"},
            },
        }
    }
    try:
        db.create_collection("movies", validator=movies_validator)
    except CollectionInvalid:
        logging.info("Коллекция 'movies' уже существует")

    db.movies.create_index([("title", pymongo.ASCENDING)])

    try:
        client.admin.command("shardCollection", f"{db.name}.movies", key={"_id": "hashed"})
    except OperationFailure as exc:
        logging.error("Ошибка шардирования коллекции 'movies': %s", exc)


def init_ratings(db: pymongo.database.Database, client: pymongo.MongoClient) -> None:
    ratings_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "movie_id", "rating", "created_at"],
            "properties": {
                "_id": {"bsonType": "objectId", "description": "Уникальный идентификатор документа"},
                "user_id": {"bsonType": "objectId", "description": "Ссылка на users._id"},
                "movie_id": {"bsonType": "objectId", "description": "Ссылка на movies._id"},
                "rating": {"bsonType": "int", "minimum": 0, "maximum": 10, "description": "Оценка (от 0 до 10)"},
                "created_at": {"bsonType": "date", "description": "Время выставления оценки"},
            },
        }
    }
    try:
        db.create_collection("ratings", validator=ratings_validator)
    except CollectionInvalid:
        logging.info("Коллекция 'ratings' уже существует")

    db.ratings.create_index(
        [("user_id", pymongo.ASCENDING), ("movie_id", pymongo.ASCENDING)],
        unique=True
    )

    try:
        client.admin.command("shardCollection", f"{db.name}.ratings", key={"user_id": 1, "movie_id": 1})
    except OperationFailure as exc:
        logging.error("Ошибка шардирования коллекции 'ratings': %s", exc)


def init_favorites(db: pymongo.database.Database, client: pymongo.MongoClient) -> None:
    favorites_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "movie_id", "created_at"],
            "properties": {
                "_id": {"bsonType": "objectId", "description": "Уникальный идентификатор"},
                "user_id": {"bsonType": "objectId", "description": "Ссылка на _id пользователя"},
                "movie_id": {"bsonType": "objectId", "description": "Ссылка на _id фильма"},
                "created_at": {"bsonType": "date", "description": "Время добавления в избранное"},
            },
        }
    }
    try:
        db.create_collection("favorites", validator=favorites_validator)
    except CollectionInvalid:
        logging.info("Коллекция 'favorites' уже существует")

    db.favorites.create_index(
        [("user_id", pymongo.ASCENDING), ("movie_id", pymongo.ASCENDING)],
        unique=True
    )

    try:
        client.admin.command("shardCollection", f"{db.name}.favorites", key={"user_id": 1, "movie_id": 1})
    except OperationFailure as exc:
        logging.error("Ошибка шардирования коллекции 'favorites': %s", exc)


def init_reviews(db: pymongo.database.Database, client: pymongo.MongoClient) -> None:
    reviews_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "movie_id", "review_text", "created_at"],
            "properties": {
                "_id": {"bsonType": "objectId", "description": "Уникальный идентификатор отзыва"},
                "user_id": {"bsonType": "objectId", "description": "Ссылка на _id пользователя"},
                "movie_id": {"bsonType": "objectId", "description": "Ссылка на _id фильма"},
                "review_text": {"bsonType": "string", "description": "Текст отзыва"},
                "created_at": {"bsonType": "date", "description": "Время создания отзыва"},
            },
        }
    }
    try:
        db.create_collection("reviews", validator=reviews_validator)
    except CollectionInvalid:
        logging.info("Коллекция 'reviews' уже существует")

    db.reviews.create_index([("user_id", pymongo.ASCENDING), ("movie_id", pymongo.ASCENDING)])

    try:
        client.admin.command("shardCollection", f"{db.name}.reviews", key={"_id": "hashed"})
    except OperationFailure as exc:
        logging.error("Ошибка шардирования коллекции 'reviews': %s", exc)


def init_review_likes(db: pymongo.database.Database, client: pymongo.MongoClient) -> None:
    review_likes_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["review_id", "user_id", "is_like", "created_at"],
            "properties": {
                "_id": {"bsonType": "objectId", "description": "Уникальный идентификатор"},
                "review_id": {"bsonType": "objectId", "description": "Ссылка на reviews._id"},
                "user_id": {"bsonType": "objectId", "description": "Ссылка на users._id"},
                "is_like": {"bsonType": "bool", "description": "Лайк (true) или дизлайк (false)"},
                "created_at": {"bsonType": "date", "description": "Время установки лайка/дизлайка"},
            },
        }
    }
    try:
        db.create_collection("review_likes", validator=review_likes_validator)
    except CollectionInvalid:
        logging.info("Коллекция 'review_likes' уже существует")

    db.review_likes.create_index(
        [("review_id", pymongo.ASCENDING), ("user_id", pymongo.ASCENDING)],
        unique=True
    )

    try:
        client.admin.command("shardCollection", f"{db.name}.review_likes", key={"review_id": 1, "user_id": 1})
    except OperationFailure as exc:
        logging.error("Ошибка шардирования коллекции 'review_likes': %s", exc)


def initialize_mongo_schema(connection_dsl: Dict[str, str]) -> None:
    db = get_mongo_db(connection_dsl)
    client = db.client
    db_name = db.name

    enable_sharding(client, db_name)
    init_users(db, client)
    init_movies(db, client)
    init_ratings(db, client)
    init_favorites(db, client)
    init_reviews(db, client)
    init_review_likes(db, client)


if __name__ == "__main__":
    initialize_mongo_schema(mongo_dsl)
