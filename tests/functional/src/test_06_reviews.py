from http import HTTPStatus
from typing import Any, Awaitable, Callable, Dict

import pytest
from config import settings

pytestmark = pytest.mark.asyncio

review_id = ""


@pytest.mark.parametrize(
    "post_body, exp_status, exp_result",
    [
        pytest.param(
            {
                "review_text": "example review text 2",
                "film_score": 10,
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
    Добавление второй рецензии к фильму.
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
            10,
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
    Получение списка рецензий к фильму.
    Должно быть две рецензии.
    """
    response = await make_get_request(
        settings.UGC2_SERVICE_URL
        + "/api/v1/reviews/"
        + settings.EXAMPLE_FILM_ID
    )
    body = await response.json()
    assert response.status == exp_status
    assert len(body) == 2
    assert "created_at" in body[0]
    assert "id" in body[0]
    assert "film_score" in body[0]
    assert "likes" in body[0]

    # запоминаем вторую рецензию из списка
    global review_id
    review_id = body[1].get("id")


@pytest.mark.parametrize(
    "post_body, exp_status, exp_result",
    [
        pytest.param(
            {},
            HTTPStatus.OK,
            HTTPStatus.OK,
            id="like review",
        ),
    ],
)
async def test_like_review(
    make_post_request: Callable[[str, Dict[str, Any]], Awaitable[Any]],
    post_body: Dict[str, Any],
    exp_status: HTTPStatus,
    exp_result: str | None,
) -> None:
    """
    Ставим лайк к одной рецензии.
    """
    response = await make_post_request(
        settings.UGC2_SERVICE_URL + "/api/v1/reviews/" + review_id + "/like",
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
            10,
            id="get reviews",
        ),
    ],
)
async def test_get_reviews2(
    make_get_request: Callable[[str], Awaitable[Any]],
    post_body: Dict[str, Any],
    exp_status: HTTPStatus,
    exp_result: str | None,
) -> None:
    """
    Получаем список рецензий и проверяем,
    что на первом месте находится рецензия с лайком,
    которая ранее была вторая в списке.
    """
    response = await make_get_request(
        settings.UGC2_SERVICE_URL
        + "/api/v1/reviews/"
        + settings.EXAMPLE_FILM_ID
    )
    body = await response.json()
    assert response.status == exp_status
    assert len(body) == 2

    first_review = body[0]

    assert "created_at" in first_review
    assert "id" in first_review
    assert "film_score" in first_review
    assert "likes" in first_review
    assert first_review.get("likes") == 1
