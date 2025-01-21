import asyncio
from typing import Any, AsyncGenerator, Callable, Coroutine, Dict

import aiohttp
import pytest_asyncio


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """
    Фикстура, предоставляющая цикл событий asyncio для сессии тестирования.

    Возвращает:
        asyncio.AbstractEventLoop: Цикл событий для использования в тестах.
    """
    loop = asyncio.get_event_loop()
    yield loop
    # loop.close()


@pytest_asyncio.fixture(name="aiohttp_client", scope="session")
async def aiohttp_client() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """
    Фикстура, создающая и управляющая сессией aiohttp ClientSession.

    Используется для выполнения HTTP-запросов в тестах.

    Возвращает:
        AsyncGenerator[aiohttp.ClientSession, None]: Асинхронный генератор,
        который предоставляет сессию aiohttp для выполнения запросов.
    """
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name="make_get_request")
def make_get_request(
    aiohttp_client: aiohttp.ClientSession,
) -> Callable[[str], Coroutine[Any, Any, aiohttp.ClientResponse]]:
    """
    Фикстура, предоставляющая функцию для выполнения GET-запросов к сервису.

    Используется для выполнения GET-запросов к API.

    Параметры:
        aiohttp_client (aiohttp.ClientSession): Сессия aiohttp.

    Возвращает:
        Callable[[str, str], aiohttp.ClientResponse]: Функция,
        принимающая имя сервиса и данные для запроса,
        возвращающая ответ от сервиса.
    """

    async def inner(url: str) -> aiohttp.ClientResponse:
        response = await aiohttp_client.get(url)
        return response

    return inner


@pytest_asyncio.fixture(name="make_post_request")
def make_post_request(
    aiohttp_client: aiohttp.ClientSession,
) -> Callable[
    [str, dict[str, Any]], Coroutine[Any, Any, aiohttp.ClientResponse]
]:
    async def inner(url: str, data: Dict[str, Any]) -> aiohttp.ClientResponse:
        return await aiohttp_client.post(url, json=data)

    return inner


@pytest_asyncio.fixture(name="make_put_request")
def make_put_request(
    aiohttp_client: aiohttp.ClientSession,
) -> Callable[[str, str], Coroutine[Any, Any, aiohttp.ClientResponse]]:
    async def inner(url: str, data: str) -> aiohttp.ClientResponse:
        return await aiohttp_client.post(url, json=data)

    return inner


@pytest_asyncio.fixture(name="make_delete_request")
def make_delete_request(
    aiohttp_client: aiohttp.ClientSession,
) -> Callable[[str], Coroutine[Any, Any, aiohttp.ClientResponse]]:
    async def inner(url: str) -> aiohttp.ClientResponse:
        return await aiohttp_client.delete(url)

    return inner
