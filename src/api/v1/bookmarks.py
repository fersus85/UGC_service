import logging
from uuid import UUID

from fastapi import APIRouter, Path, status
from fastapi.params import Depends

from services.bookmark_service import BookmarksService, get_bookmark_service
from utils.helpers import get_user_id_from_access_token

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
    film_id: UUID = Path(
        title="UUID фильма", example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    ),
    user_id: str = Depends(get_user_id_from_access_token),
    bookmark_service: BookmarksService = Depends(get_bookmark_service),
) -> None:
    """
    Добавляет фильм в закладки
    """
    await bookmark_service.add_film_to_bookmarks(film_id, user_id)
    return None


@router.delete(
    "/{film_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete bookmark",
    description="Удаляет фильм из закладок",
)
async def delete_film_from_bookmark(
    film_id: UUID = Path(
        title="UUID фильма", example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    ),
    user_id: str = Depends(get_user_id_from_access_token),
    bookmark_service: BookmarksService = Depends(get_bookmark_service),
) -> None:
    """
    Удаляет фильм из закладок
    """
    await bookmark_service.delete_film_from_bookmarks(film_id, user_id)
    return None
