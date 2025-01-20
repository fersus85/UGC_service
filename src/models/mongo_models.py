from datetime import datetime, timezone
from uuid import UUID, uuid4

import pymongo
from beanie import Document
from pydantic import Field
from pymongo import IndexModel


class FilmScoreModel(Document):
    """
    Модель таблицы с оценками фильмов.
    """

    id: UUID = Field(default_factory=uuid4)
    film_id: UUID
    user_id: UUID
    film_score: int = Field(..., ge=0, le=10)

    class Settings:
        name = "film_scores"
        indexes = [
            IndexModel(
                [
                    ("film_id", pymongo.ASCENDING),
                    ("user_id", pymongo.ASCENDING),
                ],
                name="film_user_idx",
                unique=True,
            ),
        ]


class FilmBookmarkModel(Document):
    """
    Модель таблицы с пользовательскими закладками фильмов.
    """

    id: UUID = Field(default_factory=uuid4)
    film_id: UUID
    user_id: UUID

    class Settings:
        name = "film_bookmarks"
        indexes = [
            IndexModel(
                [
                    ("user_id", pymongo.ASCENDING),
                    ("film_id", pymongo.ASCENDING),
                ],
                name="user_film_idx",
                unique=True,
            ),
        ]


class FilmReviewModel(Document):
    """
    Модель таблицы с пользовательскими отзывами на фильмы.
    """

    id: UUID = Field(default_factory=uuid4)
    film_id: UUID
    user_id: UUID
    review_text: str
    film_score: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "film_reviews"
        indexes = [
            IndexModel(
                [
                    ("film_id", pymongo.ASCENDING),
                    ("user_id", pymongo.ASCENDING),
                ],
                name="film_user_idx",
                unique=True,
            ),
        ]


class ReviewLikeModel(Document):
    """
    Модель таблицы с лайками на отзывы.
    """

    id: UUID = Field(default_factory=uuid4)
    review_id: UUID
    user_id: UUID

    class Settings:
        name = "review_likes"
        indexes = [
            IndexModel(
                [
                    ("review_id", pymongo.ASCENDING),
                    ("film_id", pymongo.ASCENDING),
                ],
                name="review_user_idx",
                unique=True,
            ),
        ]
