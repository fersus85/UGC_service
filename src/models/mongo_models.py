from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from beanie import Document, before_event, Insert
from pydantic import Field
from pymongo import ASCENDING, IndexModel

from db.casher import get_cacher


async def get_next_counter(key: str) -> int:
    cacher = await get_cacher()
    return await cacher.incr(key, 1)


class MonotonicSequenceMixin:
    monotonic_seq: Optional[int] = None

    @classmethod
    def get_redis_key(cls) -> str:
        return f"UGC_service:src:models:mongo_models:{cls.__name__}:counter"

    @before_event(Insert)
    async def set_monotonic_seq(self):
        key = self.get_redis_key()
        self.monotonic_seq = await get_next_counter(key)


class FilmScoreModel(MonotonicSequenceMixin, Document):
    """
    Модель таблицы с оценками фильмов.
    """

    # https://github.com/BeanieODM/beanie/issues/336
    id: UUID = Field(default_factory=uuid4)  # type: ignore
    film_id: UUID
    user_id: UUID
    film_score: int = Field(..., ge=0, le=10)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

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


class FilmBookmarkModel(MonotonicSequenceMixin, Document):
    """
    Модель таблицы с пользовательскими закладками фильмов.
    """

    id: UUID = Field(default_factory=uuid4)  # type: ignore
    film_id: UUID
    user_id: UUID
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

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


class FilmReviewModel(MonotonicSequenceMixin, Document):
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


class ReviewLikeModel(MonotonicSequenceMixin, Document):
    """
    Модель таблицы с лайками на отзывы.
    """

    id: UUID = Field(default_factory=uuid4)  # type: ignore
    review_id: UUID
    user_id: UUID
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "review_likes"
        indexes = [
            IndexModel(
                [
                    ("review_id", ASCENDING),
                    ("user_id", ASCENDING),
                ],
                name="review_user_idx",
                unique=True,
            ),
        ]
