import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from init_services import init_casher, init_mongo

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Иницилизирует сервисы перед стартом
    приложения и зыкрывает соединения после
    """

    await init_casher()
    await init_mongo()

    logger.info("App is ready")

    yield

    logger.debug("App is closing...")
