from http import HTTPStatus
from typing import Any, Callable, Dict

import pytest
from aiohttp import ClientResponse
from config import settings

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "post_body, exp_status, exp_result",
    [
        pytest.param(
            {},
            HTTPStatus.CREATED,
            HTTPStatus.CREATED,
            id="add bookmark",
        ),
    ],
)
async def test_add_bookmark(
    make_post_request: Callable[[str, str, Dict[str, Any]], ClientResponse],
    post_body: Dict[str, Any],
    exp_status: HTTPStatus,
    exp_result: str | None,
) -> None:
    """
    Добавление фильма в закладки.
    """
    response = await make_post_request(
        settings.UGC2_SERVICE_URL
        + "/api/v1/bookmarks/"
        + settings.EXAMPLE_FILM_ID,
        post_body,
    )
    body = await response.json()
    assert response.status == exp_status
    assert body == exp_result


@pytest.mark.parametrize(
    "post_body, exp_status, exp_result",
    [
        pytest.param(
            {},
            HTTPStatus.OK,
            [settings.EXAMPLE_FILM_ID],
            id="get bookmarks",
        ),
    ],
)
async def test_get_bookmarks(
    make_get_request: Callable[[str, str, Dict[str, Any]], ClientResponse],
    post_body: Dict[str, Any],
    exp_status: HTTPStatus,
    exp_result: str | None,
) -> None:
    """
    Получение списка фильмов в закладках.
    """
    response = await make_get_request(
        settings.UGC2_SERVICE_URL + "/api/v1/bookmarks/"
    )
    body = await response.json()
    assert response.status == exp_status
    assert body == exp_result


@pytest.mark.parametrize(
    "post_body, exp_status, exp_result",
    [
        pytest.param(
            {},
            HTTPStatus.NO_CONTENT,
            None,
            id="delete bookmarks",
        ),
    ],
)
async def test_del_bookmarks(
    make_delete_request: Callable[[str, str, Dict[str, Any]], ClientResponse],
    post_body: Dict[str, Any],
    exp_status: HTTPStatus,
    exp_result: str | None,
) -> None:
    """
    Удаление фильма из закладок.
    """
    response = await make_delete_request(
        settings.UGC2_SERVICE_URL
        + "/api/v1/bookmarks/"
        + settings.EXAMPLE_FILM_ID,
    )
    body = await response.json()
    assert response.status == exp_status
    assert body == exp_result


@pytest.mark.parametrize(
    "post_body, exp_status, exp_result",
    [
        pytest.param(
            {},
            HTTPStatus.OK,
            [],
            id="get bookmarks",
        ),
    ],
)
async def test_get_bookmarks_empty(
    make_get_request: Callable[[str, str, Dict[str, Any]], ClientResponse],
    post_body: Dict[str, Any],
    exp_status: HTTPStatus,
    exp_result: str | None,
) -> None:
    """
    Получение пустого списка закладок после удаления.
    """
    response = await make_get_request(
        settings.UGC2_SERVICE_URL + "/api/v1/bookmarks/"
    )
    body = await response.json()
    assert response.status == exp_status
    assert body == exp_result
