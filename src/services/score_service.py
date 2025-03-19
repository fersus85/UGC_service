import logging
from functools import lru_cache
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from models.mongo_models import FilmReviewModel, FilmScoreModel
from schemas.scores import AddScore

logger = logging.getLogger(__name__)


class FilmScoreService:
    """
    Сервис для работы с оценками фильмов в MongoDB.
    """

    def __init__(
        self,
    ):
        """
        Инициализирует сервис оценок фильмов.
        """
        pass

    async def add_score(
        self, film_id: str, user_id: str, film_score: int
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
                FilmScoreModel.film_id == UUID(film_id),
            )
            if existing_film_score:
                existing_film_score.film_score = film_score
                await existing_film_score.save()

        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error while adding film score: {ex}",
            ) from ex

        existing_film_review = await FilmReviewModel.find_one(
            FilmScoreModel.user_id == UUID(user_id),
            FilmScoreModel.film_id == UUID(film_id),
        )
        if existing_film_review:
            existing_film_review.film_score = film_score
            await existing_film_review.save()

    async def delete_score(
        self,
        film_id: str,
        user_id: str,
    ) -> None:
        """
        Удаляет оценку фильма.
        """
        try:
            await FilmScoreModel.find_one(
                FilmScoreModel.user_id == UUID(user_id),
                FilmScoreModel.film_id == UUID(film_id),
            ).delete()
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error while deleting film score: {ex}",
            ) from ex

    async def get_score(
        self,
        film_id: str,
    ) -> float | None:
        """
        Возвращает среднюю оценку фильма.
        """

        avg_score = await FilmScoreModel.find(
            FilmScoreModel.film_id == UUID(film_id),
        ).avg(FilmScoreModel.film_score)
        return avg_score

    async def get_user_scores(self, user_id: str) -> List[AddScore]:
        try:
            user_uuid = UUID(user_id)
            film_scores = await FilmScoreModel.find(
                FilmScoreModel.user_id == user_uuid
            ).to_list()
            return [AddScore(film_id=str(fs.film_id), film_score=fs.film_score) for fs in film_scores]
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при получении оценок пользователя: {ex}",
            ) from ex


@lru_cache
def get_film_score_service() -> FilmScoreService:
    """
    Возвращает экземпляр сервиса для работы с оценками фильмов.
    """
    return FilmScoreService()
