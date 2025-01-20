import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

import db.casher as cacher
from core.config import settings
from db import mongo, redis
from models.mongo_models import (
    FilmBookmarkModel,
    FilmReviewModel,
    FilmScoreModel,
    ReviewLikeModel,
)

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

        db_name = settings.MONGO_DB + "_new"

        await init_beanie(
            database=mongo_client[db_name],
            document_models=[
                FilmScoreModel,
                FilmBookmarkModel,
                FilmReviewModel,
                ReviewLikeModel,
            ],
        )

        mongo.mongo_repository = mongo.MongoRepository(mongo_client)

        logger.info("Connected to MongoDB successfully.")

    except Exception as ex:

        logger.exception(f"Error connecting to MongoDB: {ex}")
