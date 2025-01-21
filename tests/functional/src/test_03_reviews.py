from http import HTTPStatus
from typing import Any, Awaitable, Callable, Dict

import pytest
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
    make_post_request: Callable[[str, Dict[str, Any]], Awaitable[Any]],
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
    make_get_request: Callable[[str], Awaitable[Any]],
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

    first_review = body[0]

    assert "created_at" in first_review
    assert "id" in first_review
    assert "film_score" in first_review
    assert "likes" in first_review
    assert first_review.get("film_score") == exp_result
