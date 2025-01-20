from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class FilmReview(BaseModel):
    """
    Модель ответа пользователю о рецензии и оценке фильма.
    """

    id: UUID
    user_id: UUID
    review_text: str
    film_score: int = Field(..., ge=1, le=10)
    created_at: datetime


class FilmReviewPost(BaseModel):
    """
    Модель для добавления и обновления отзыва и оценки фильма.
    """

    review_text: str
    film_score: int = Field(..., ge=1, le=10)
