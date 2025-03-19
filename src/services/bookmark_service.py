from functools import lru_cache
from uuid import UUID

from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from models.mongo_models import FilmBookmarkModel
from schemas.bookmarks import FilmBookmarkGRPC


class BookmarksService:
    """
    Сервис для работы с закладками фильмов в MongoDB.
    """

    def __init__(self) -> None:
        """
        Инициализирует сервис закладок фильмов.
        """
        pass

    async def get_bookmark_films(self, user_id: str) -> list[UUID]:
        """
        Возвращает список id фильмов, добавленных пользователем в закладки.
        """
        try:
            bookmarks_list = await FilmBookmarkModel.find(
                FilmBookmarkModel.user_id == UUID(user_id),
            ).to_list()
            return [bookmark.film_id for bookmark in bookmarks_list]
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error finding film bookmarks: {ex}",
            ) from ex

    async def get_bookmark_films_schema(self, user_id: str) -> list[FilmBookmarkGRPC]:
        try:
            bookmarks_list = await FilmBookmarkModel.find(
                FilmBookmarkModel.user_id == UUID(user_id),
            ).to_list()
            return [FilmBookmarkGRPC(
                film_id=str(bookmark.film_id),
                created_at=bookmark.created_at
            ) for bookmark in bookmarks_list]
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error finding film bookmarks: {ex}",
            ) from ex

    async def add_film_to_bookmarks(self, film_id: str, user_id: str) -> None:
        """
        Добавляет фильм в закладки.
        """
        try:
            await FilmBookmarkModel(
                film_id=UUID(film_id), user_id=UUID(user_id)
            ).insert()
        except DuplicateKeyError:
            pass
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error while adding film bookmark: {ex}",
            ) from ex

    async def delete_film_from_bookmarks(
        self, film_id: str, user_id: str
    ) -> None:
        """
        Удаляет фильм из закладок пользователя.
        """
        try:
            await FilmBookmarkModel.find_one(
                FilmBookmarkModel.user_id == UUID(user_id),
                FilmBookmarkModel.film_id == UUID(film_id),
            ).delete()
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error while deleting film bookmark: {ex}",
            ) from ex


@lru_cache
def get_bookmark_service() -> BookmarksService:
    """
    Возвращает экземпляр сервиса для работы с закладками фильмов.
    """
    return BookmarksService()
