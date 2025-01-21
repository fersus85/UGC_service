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
                "review_text": "example review text",
                "film_score": 1,
            },
            HTTPStatus.CREATED,
            HTTPStatus.CREATED,
            id="add review",
        ),
    ],
)
async def test_add_review(
    make_post_request: Callable[[str, str, Dict[str, Any]], ClientResponse],
    post_body: Dict[str, Any],
    exp_status: HTTPStatus,
    exp_result: str | None,
) -> None:
    """
    Добавление рецензии к фильму.
    """
    response = await make_post_request(
        settings.UGC2_SERVICE_URL
        + "/api/v1/reviews/"
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
            1,
            id="get reviews",
        ),
    ],
)
async def test_get_reviews(
    make_get_request: Callable[[str, str, Dict[str, Any]], ClientResponse],
    post_body: Dict[str, Any],
    exp_status: HTTPStatus,
    exp_result: str | None,
) -> None:
    """
    Получение спискарецензий фильма.
    Кол-во должно быть равно одному.
    """
    response = await make_get_request(
        settings.UGC2_SERVICE_URL
        + "/api/v1/reviews/"
        + settings.EXAMPLE_FILM_ID
    )
    body = await response.json()
    assert response.status == exp_status
    assert len(body) == 1
    assert "created_at" in body[0]
    assert "id" in body[0]
    assert "film_score" in body[0]
    assert "likes" in body[0]
    assert body[0].get("film_score") == exp_result
