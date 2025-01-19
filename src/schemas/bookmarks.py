from uuid import UUID

from pydantic import BaseModel


class FilmBookmark(BaseModel):
    """Модель для добавления фильма в закладки."""

    film_id: UUID
