import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from services.bookmark_service import BookmarksService, get_bookmark_service
from utils.token_helpers import get_user_id_from_access_token

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/bookmarks",
    tags=["Bookmarks"],
)


@router.get(
    "/",
    response_model=list[UUID],
    summary="Get bookmark list",
    description="Возвращает закладки фильмов пользователя",
)
async def get_film_bookmarks(
    user_id: str = Depends(get_user_id_from_access_token),
    bookmark_service: BookmarksService = Depends(get_bookmark_service),
) -> list[UUID]:
    """
    Возвращает закладки фильмов пользователя
    Параметры:
        user_id: str - ID пользователя
    """
    films_ids = await bookmark_service.get_bookmark_films(user_id)
    return films_ids


@router.post(
    "/{film_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add bookmark",
    description="Добавляет фильм в закладки",
)
async def add_film_to_bookmark(
    film_id: str = Path(
        title="ID фильма", examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
    ),
    user_id: str = Depends(get_user_id_from_access_token),
    bookmark_service: BookmarksService = Depends(get_bookmark_service),
) -> int:
    """
    Добавляет фильм в закладки
    Параметры:
        film_id: str - ID фильма
        user_id: str - ID пользователя

    """
    await bookmark_service.add_film_to_bookmarks(film_id, user_id)
    return status.HTTP_201_CREATED


@router.delete(
    "/{film_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete bookmark",
    description="Удаляет фильм из закладок",
)
async def delete_film_from_bookmark(
    film_id: str = Path(
        title="UUID фильма", examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
    ),
    user_id: str = Depends(get_user_id_from_access_token),
    bookmark_service: BookmarksService = Depends(get_bookmark_service),
) -> None:
    """
    Удаляет фильм из закладок
    Параметры:
        film_id: str - ID фильма
    """
    await bookmark_service.delete_film_from_bookmarks(film_id, user_id)
    return None
