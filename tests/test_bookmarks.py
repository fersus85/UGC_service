from unittest.mock import AsyncMock, patch

import pytest

from tests.init_client import client

pytestmark = pytest.mark.asyncio


@patch(
    "services.bookmark_service.BookmarksService.get_bookmark_films",
    new_callable=AsyncMock,
)
async def test_get_bookmark_films(get_bookmark_films: AsyncMock):
    get_bookmark_films.return_value = []

    response = client.get(
        "/api/v1/bookmarks/",
    )

    assert response.status_code == 200
    assert response.json() == []
    assert get_bookmark_films.call_count == 1
