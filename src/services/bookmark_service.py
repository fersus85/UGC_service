from functools import lru_cache
from uuid import UUID

from fastapi import Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from db.mongo import MongoRepository, get_mongo_repository
from models.mongo_models import FilmBookmarkModel


class BookmarksService:
    """
    Сервис для работы с закладками фильмов в MongoDB.
    """

    def __init__(self, mongo_repository: MongoRepository) -> None:
        """
        Инициализирует сервис закладок фильмов.
        """
        self._mongo_repository = mongo_repository
        self.collection_name = "film_bookmarks"

    async def get_bookmark_films(self, user_id: UUID) -> list[UUID] | None:
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

    async def add_film_to_bookmarks(
        self, film_id: UUID, user_id: UUID
    ) -> None:
        """
        Добавляет фильм в закладки.
        """
        try:
            await FilmBookmarkModel(film_id=film_id, user_id=user_id).insert()
        except DuplicateKeyError:
            pass
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error while adding film bookmark: {ex}",
            ) from ex

    async def delete_film_from_bookmarks(
        self, film_id: UUID, user_id: UUID
    ) -> None:
        """
        Удаляет фильм из закладок пользователя.
        """
        try:
            await FilmBookmarkModel.find_one(
                FilmBookmarkModel.user_id == UUID(user_id),
                FilmBookmarkModel.film_id == UUID(str(film_id)),
            ).delete()
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error while deleting film bookmark: {ex}",
            ) from ex


@lru_cache
def get_bookmark_service(
    repository=Depends(get_mongo_repository),
) -> BookmarksService:
    """
    Возвращает экземпляр сервиса для работы с закладками фильмов.
    """
    return BookmarksService(repository)
