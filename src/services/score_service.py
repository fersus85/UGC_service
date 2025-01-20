import logging
import uuid
from functools import lru_cache
from uuid import UUID

from fastapi import Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from db.mongo import MongoRepository, get_mongo_repository
from models.mongo_models import FilmReviewModel, FilmScoreModel

logger = logging.getLogger(__name__)


class FilmScoreService:
    """
    Сервис для работы с оценками фильмов в MongoDB.
    """

    def __init__(self, mongo_repository: MongoRepository):
        """
        Инициализирует сервис оценок фильмов.
        """
        self._mongo_repository = mongo_repository
        self.collection_name = "film_score"

    async def add_score(
        self, film_id: UUID, user_id: UUID, film_score: int
    ) -> None:
        """
        Добавляет или обновляет оценку фильма.
        """
        try:

            await FilmScoreModel(
                film_id=film_id, user_id=user_id, film_score=film_score
            ).insert()

        except DuplicateKeyError:
            existing_film_score = await FilmScoreModel.find_one(
                FilmScoreModel.user_id == UUID(user_id),
                FilmScoreModel.film_id == UUID(str(film_id)),
            )
            existing_film_score.film_score = film_score
            await existing_film_score.save()

        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error while adding film score: {ex}",
            ) from ex

        existing_film_review = await FilmReviewModel.find_one(
            FilmScoreModel.user_id == UUID(user_id),
            FilmScoreModel.film_id == UUID(str(film_id)),
        )
        if existing_film_review:
            existing_film_review.film_score = film_score
            await existing_film_review.save()

    async def delete_score(
        self,
        film_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:
        """
        Удаляет оценку фильма.
        """
        try:
            await FilmScoreModel.find_one(
                FilmScoreModel.user_id == UUID(user_id),
                FilmScoreModel.film_id == UUID(str(film_id)),
            ).delete()
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error while deleting film score: {ex}",
            ) from ex

    async def get_score(
        self,
        film_id: uuid.UUID,
    ) -> float | None:
        """
        Возвращает среднюю оценку фильма.
        """

        avg_score = await FilmScoreModel.find(
            FilmScoreModel.film_id == UUID(str(film_id)),
        ).avg(FilmScoreModel.film_score)
        return avg_score


@lru_cache
def get_film_score_service(
    repository: MongoRepository = Depends(get_mongo_repository),
) -> FilmScoreService:
    """
    Возвращает экземпляр сервиса для работы с оценками фильмов.
    """
    return FilmScoreService(repository)
