from unittest.mock import AsyncMock, patch

import pytest

from tests.init_client import client

pytestmark = pytest.mark.asyncio


@patch(
    "services.score_service.FilmScoreService.get_score",
    new_callable=AsyncMock,
)
async def test_get_score(get_score: AsyncMock):
    """
    Получение средней оценки фильма.
    """
    get_score.return_value = 10

    response = client.get(
        "/api/v1/scores/3fa85f64-5717-4562-b3fc-2c963f66afa6",
    )

    assert response.status_code == 200
    assert response.json() == {"average_score": 10.0}
    assert get_score.call_count == 1


@patch(
    "services.score_service.FilmScoreService.add_score",
    new_callable=AsyncMock,
)
async def test_add_score(add_score: AsyncMock):
    """
    Добавление оценки фильма.
    """
    add_score.return_value = None

    data: dict = {
        "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "film_score": 10,
    }

    response = client.post("/api/v1/scores/", json=data)

    assert response.status_code == 201
    assert response.json() == 201
    assert add_score.call_count == 1


@patch(
    "services.score_service.FilmScoreService.delete_score",
    new_callable=AsyncMock,
)
async def test_del_score(delete_score: AsyncMock):
    """
    Удаление оценки фильма.
    """
    delete_score.return_value = None

    response = client.delete(
        "/api/v1/scores/3fa85f64-5717-4562-b3fc-2c963f66afa6/"
    )

    assert response.status_code == 204
    assert delete_score.call_count == 1
