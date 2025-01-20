from datetime import datetime, timezone
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field
from pymongo import IndexModel, ASCENDING


class FilmScoreModel(Document):
    """
    Модель таблицы с оценками фильмов.
    """

    # https://github.com/BeanieODM/beanie/issues/336
    id: UUID = Field(default_factory=uuid4)  # type: ignore
    film_id: UUID
    user_id: UUID
    film_score: int = Field(..., ge=0, le=10)

    class Settings:
        name = "film_scores"
        indexes = [
            IndexModel(
                [
                    ("film_id", ASCENDING),
                    ("user_id", ASCENDING),
                ],
                name="film_user_idx",
                unique=True,
            ),
        ]


class FilmBookmarkModel(Document):
    """
    Модель таблицы с пользовательскими закладками фильмов.
    """

    id: UUID = Field(default_factory=uuid4)  # type: ignore
    film_id: UUID
    user_id: UUID

    class Settings:
        name = "film_bookmarks"
        indexes = [
            IndexModel(
                [
                    ("user_id", ASCENDING),
                    ("film_id", ASCENDING),
                ],
                name="user_film_idx",
                unique=True,
            ),
        ]


class FilmReviewModel(Document):
    """
    Модель таблицы с пользовательскими отзывами на фильмы.
    """

    id: UUID = Field(default_factory=uuid4)  # type: ignore
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
                    ("film_id", ASCENDING),
                    ("user_id", ASCENDING),
                ],
                name="film_user_idx",
                unique=True,
            ),
        ]


class ReviewLikeModel(Document):
    """
    Модель таблицы с лайками на отзывы.
    """

    id: UUID = Field(default_factory=uuid4)  # type: ignore
    review_id: UUID
    user_id: UUID

    class Settings:
        name = "review_likes"
        indexes = [
            IndexModel(
                [
                    ("review_id", ASCENDING),
                    ("film_id", ASCENDING),
                ],
                name="review_user_idx",
                unique=True,
            ),
        ]
