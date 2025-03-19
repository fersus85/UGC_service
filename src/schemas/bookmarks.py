from datetime import datetime

from pydantic import BaseModel, Field


class FilmBookmark(BaseModel):
    """Модель для добавления фильма в закладки."""

    film_id: str = Field(
        ...,
        description="UUID фильма",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )


class FilmBookmarkGRPC(FilmBookmark):
    created_at: datetime
