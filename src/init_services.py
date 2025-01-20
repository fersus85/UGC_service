import logging

from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

import db.casher as cacher
from core.config import settings
from db import mongo, redis

logger = logging.getLogger(__name__)


async def init_casher():
    try:
        redis.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        cacher.cacher = redis.RedisCache(redis.redis)
    except Exception as ex:
        logger.exception(f"Error connecting to Redis: {ex}")


async def init_mongo():

    try:

        mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(
            settings.MONGO_HOST
        )
        db = mongo_client[settings.MONGO_DB]

        if "film_bookmarks" not in await db.list_collection_names():
            collection = db["film_bookmarks"]
            collection.create_index(
                [("film_id", 1), ("user_id", 1)], unique=True
            )
        if "film_scores" not in await db.list_collection_names():
            collection = db["film_score"]
            collection.create_index(
                [("film_id", 1), ("user_id", 1)], unique=True
            )
        if "film_reviews" not in await db.list_collection_names():
            collection = db["film_reviews"]
            collection.create_index(
                [("film_id", 1), ("user_id", 1)], unique=True
            )

        mongo.mongo_repository = mongo.MongoRepository(mongo_client)

        logger.info("Connected to MongoDB successfully.")

    except Exception as ex:

        logger.exception(f"Error connecting to MongoDB: {ex}")
