import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis

import db.casher as cacher
from core.config import settings
from db import redis
from db.mongo import mongo_storage

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Иницилизирует сервисы перед стартом
    приложения и зыкрывает соединения после
    """
    redis.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    cacher.cacher = redis.RedisCache(redis.redis)
    await mongo_storage.on_startup(
        [f"{settings.MONGO_HOST}:{settings.MONGO_PORT}"]
    )

    logger.info("App ready")
    yield
    await mongo_storage.on_shutdown()
    logger.debug("Closing connections")
