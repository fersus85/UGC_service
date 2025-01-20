import uuid
from functools import lru_cache
from uuid import UUID

from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from models.mongo_models import (
    FilmReviewModel,
    FilmScoreModel,
    ReviewLikeModel,
)


class ReviewsService:
    """
    Сервис для работы с отзывами фильмов в MongoDB.
    """

    def __init__(
        self,
    ):
        """
        Инициализирует сервис отзывов.
        """
        pass

    async def add_review(
        self,
        film_id: UUID,
        review_text: str,
        user_id: UUID,
        film_score: int,
    ) -> None:
        """
        Добавляет отзыв и оценку фильма.
        """
        try:

            await FilmReviewModel(
                film_id=film_id,
                user_id=user_id,
                film_score=film_score,
                review_text=review_text,
            ).insert()

        except DuplicateKeyError as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Review for this film already exists",
            ) from ex

        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error while adding film score: {ex}",
            ) from ex

        # ищем, существует ли отдельная оценка фильма
        existing_film_score = await FilmScoreModel.find_one(
            FilmScoreModel.user_id == UUID(user_id),
            FilmScoreModel.film_id == UUID(str(film_id)),
        )
        # если существует отдельная оценка - обновляем отдельную оценку
        if existing_film_score:
            existing_film_score.film_score = film_score
            await existing_film_score.save()
        # если нет отдельной оценки - добавляем
        else:
            await FilmScoreModel(
                film_id=film_id, user_id=user_id, film_score=film_score
            ).insert()

        return None

    async def delete_review(self, review_id: UUID, user_id: UUID) -> None:
        """
        Удаляет отзыв о фильме.
        """
        try:
            await FilmReviewModel.find_one(
                FilmScoreModel.id == UUID(review_id),
                FilmScoreModel.user_id == UUID(user_id),
            ).delete()
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error while deleting film review: {ex}",
            ) from ex

        return None

    async def like_review(self, review_id: UUID, user_id: UUID) -> None:
        """
        Добавляет лайк к отзыву о фильме.
        """
        try:
            await ReviewLikeModel(
                review_id=review_id,
                user_id=user_id,
            ).insert()

        except DuplicateKeyError as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This review is already liked",
            ) from ex

        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error while adding film score: {ex}",
            ) from ex

        return None

    async def get_reviews(
        self,
        film_id: uuid.UUID,
        page_number: int = 1,
        page_size: int = 50,
    ) -> list[dict[str, str]]:
        """
        Возвращает список отзвов о фильме.
        """
        try:
            review_list = (
                await FilmReviewModel.find(
                    FilmReviewModel.film_id == UUID(str(film_id)),
                )
                .skip((page_number - 1) * page_size)
                .limit(page_size)
                .to_list()
            )
            return review_list
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error finding film bookmarks: {ex}",
            ) from ex


@lru_cache
def get_review_service() -> ReviewsService:
    """
    Возвращает экземпляр сервиса для работы с отзывами фильмов.
    """
    return ReviewsService()
