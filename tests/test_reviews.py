from unittest.mock import AsyncMock, patch

import pytest

from tests.init_client import client

pytestmark = pytest.mark.asyncio


@patch(
    "services.review_service.ReviewsService.get_reviews",
    new_callable=AsyncMock,
)
async def test_get_reviews(get_reviews: AsyncMock):
    """
    Получение списка рецензий фильма.
    """

    review_list = [
        {
            "id": "12385f64-5717-4562-b3fc-2c963f66a987",
            "user_id": "abc85f64-5717-4562-b3fc-2c963f66adef",
            "review_text": "test review text",
            "film_score": 10,
            "created_at": "2025-01-30T22:22:22",
            "likes": 1,
        },
        {
            "id": "23485f64-5717-4562-b3fc-2c963f66a989",
            "user_id": "cda85f64-5717-4562-b3fc-2c963f66adeb",
            "review_text": "test review text 2",
            "film_score": 8,
            "created_at": "2025-01-30T11:11:11",
            "likes": 0,
        },
    ]

    get_reviews.return_value = review_list

    response = client.get(
        "/api/v1/reviews/3fa85f64-5717-4562-b3fc-2c963f66afa6",
    )

    assert response.status_code == 200
    assert response.json() == review_list
    assert get_reviews.call_count == 1


@patch(
    "services.review_service.ReviewsService.get_reviews",
    new_callable=AsyncMock,
)
async def test_get_reviews_invalid_data(get_reviews: AsyncMock):
    """
    Получение списка рецензий фильма - неверный формат данных из хранилища.
    """
    review_list = [
        {
            "id": "XYZ85f64-5717-4562-b3fc-2c963f66a987",
            "user_id": "abc85f64-5717-4562-b3fc-2c963f66adef",
            "review_text": "test review text",
            "film_score": 10,
            "created_at": "2025-01-30T22:22:22",
            "likes": 1,
        },
    ]

    get_reviews.return_value = review_list

    response = client.get(
        "/api/v1/reviews/3fa85f64-5717-4562-b3fc-2c963f66afa6",
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "invalid data"}


@patch(
    "services.review_service.ReviewsService.add_review",
    new_callable=AsyncMock,
)
async def test_add_review(add_review: AsyncMock):
    """
    Добавление рецензии к фильму.
    """
    add_review.return_value = None

    data: dict = {"review_text": "test review text", "film_score": 10}

    response = client.post(
        "/api/v1/reviews/3fa85f64-5717-4562-b3fc-2c963f66afa6/", json=data
    )

    assert response.status_code == 201
    assert response.json() == 201
    assert add_review.call_count == 1


@patch(
    "services.review_service.ReviewsService.like_review",
    new_callable=AsyncMock,
)
async def test_like_review(like_review: AsyncMock):
    """
    Лайк рецензии.
    """
    like_review.return_value = None

    data: dict = {}

    response = client.post(
        "/api/v1/reviews/3fa85f64-5717-4562-b3fc-2c963f66afa6/like", json=data
    )

    assert response.status_code == 200
    assert response.json() == 200
    assert like_review.call_count == 1


@patch(
    "services.review_service.ReviewsService.delete_review",
    new_callable=AsyncMock,
)
async def test_delete_review(delete_review: AsyncMock):
    """
    Удаление рецензии.
    """
    delete_review.return_value = None

    response = client.delete(
        "/api/v1/reviews/3fa85f64-5717-4562-b3fc-2c963f66afa6/"
    )

    assert response.status_code == 204
    assert delete_review.call_count == 1
