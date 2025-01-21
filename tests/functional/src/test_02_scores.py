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
            {
                "film_id": settings.EXAMPLE_FILM_ID,
                "film_score": 1,
            },
            HTTPStatus.CREATED,
            HTTPStatus.CREATED,
            id="add score",
        ),
    ],
)
async def test_add_score(
    make_post_request: Callable[[str, str, Dict[str, Any]], ClientResponse],
    post_body: Dict[str, Any],
    exp_status: HTTPStatus,
    exp_result: str | None,
) -> None:
    """
    Добавление оценки фильму.
    """
    response = await make_post_request(
        settings.UGC2_SERVICE_URL + "/api/v1/scores/",
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
            1,
            id="get bookmarks",
        ),
    ],
)
async def test_get_scores(
    make_get_request: Callable[[str, str, Dict[str, Any]], ClientResponse],
    post_body: Dict[str, Any],
    exp_status: HTTPStatus,
    exp_result: str | None,
) -> None:
    """
    Получение средней оценки фильма.
    Она должна быть равна установленной на предыдущем шаге.
    """
    response = await make_get_request(
        settings.UGC2_SERVICE_URL
        + "/api/v1/scores/"
        + settings.EXAMPLE_FILM_ID
    )
    body = await response.json()
    assert response.status == exp_status
    assert "average_score" in body
    assert body.get("average_score") == exp_result
