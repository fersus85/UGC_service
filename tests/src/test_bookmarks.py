from unittest.mock import AsyncMock, patch

import pytest

pytestmark = pytest.mark.asyncio


@patch(
    "services.bookmark_service.BookmarksService.get_bookmark_films",
    new_callable=AsyncMock,
)
async def test_get_bookmarks(get_bookmark_films: AsyncMock, client):
    """
    Получение списка фильмов в закладках пользователя.
    """
    get_bookmark_films.return_value = []

    response = client.get(
        "/api/v1/bookmarks/",
    )

    assert response.status_code == 200
    assert response.json() == []
    assert get_bookmark_films.call_count == 1


@patch(
    "services.bookmark_service.BookmarksService.add_film_to_bookmarks",
    new_callable=AsyncMock,
)
async def test_add_bookmark(add_bookmark_films: AsyncMock, client):
    """
    Добавление фильма в закладки пользователя.
    """
    add_bookmark_films.return_value = None

    data: dict = {}

    response = client.post(
        "/api/v1/bookmarks/3fa85f64-5717-4562-b3fc-2c963f66afa6/", json=data
    )

    assert response.status_code == 201
    assert response.json() == 201
    assert add_bookmark_films.call_count == 1


@patch(
    "services.bookmark_service.BookmarksService.delete_film_from_bookmarks",
    new_callable=AsyncMock,
)
async def test_del_bookmark(del_bookmark_films: AsyncMock, client):
    """
    Удаление фильма из закладок пользователя.
    """
    del_bookmark_films.return_value = None

    response = client.delete(
        "/api/v1/bookmarks/3fa85f64-5717-4562-b3fc-2c963f66afa6/"
    )

    assert response.status_code == 204
    assert del_bookmark_films.call_count == 1
