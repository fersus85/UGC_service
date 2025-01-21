from http import HTTPStatus
from typing import Any, Awaitable, Callable, Dict, List, Union

import pytest
from aiohttp import ClientResponse
from config import settings

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "post_body, exp_status, exp_result",
    [
        pytest.param(
            {
                "login": "terminator2",
                "first_name": "Oleg",
                "last_name": "Kozlov",
                "password": "Qwerty123",
            },
            [HTTPStatus.CREATED, HTTPStatus.CONFLICT],
            [None, "Record already exists"],
            id="create user",
        ),
    ],
)
async def test_signup(
    make_post_request: Callable[[str, Dict[str, Any]], Awaitable[Any]],
    post_body: Dict[str, Any],
    exp_status: List[HTTPStatus],
    exp_result: List[Union[str, None]],
) -> None:
    """
    Регистрация второго пользователя.
    """
    response = await make_post_request(
        settings.AUTH_SERVICE_URL + "/api/v1/auth/signup", post_body
    )

    body = await response.json()

    assert response.status in exp_status

    if response.status == HTTPStatus.CREATED:
        assert "id" in body
        assert "created_at" in body
        assert body.get("first_name") == post_body.get("first_name")
        assert body.get("last_name") == post_body.get("last_name", "")
    else:
        assert body.get("detail") in exp_result


@pytest.mark.parametrize(
    "post_body, exp_status, exp_result",
    [
        pytest.param(
            {"login": "terminator2", "password": "Qwerty123"},
            HTTPStatus.OK,
            None,
            id="login correctly",
        ),
    ],
)
async def test_login(
    make_post_request: Callable[[str, Dict[str, Any]], Awaitable[Any]],
    post_body: Dict[str, Any],
    exp_status: HTTPStatus,
    exp_result: str | None,
) -> None:
    """
    Вход второго пользователя.
    """
    response: ClientResponse = await make_post_request(
        settings.AUTH_SERVICE_URL + "/api/v1/auth/login", post_body
    )

    body = await response.json()

    assert response.status == exp_status

    if exp_status == HTTPStatus.CREATED:
        assert "access_token" in body
        assert "refresh_token" in body
        assert body.get("first_name") == post_body.get("first_name")
        assert body.get("last_name") == post_body.get("last_name", "")
    else:
        assert body.get("detail") == exp_result
