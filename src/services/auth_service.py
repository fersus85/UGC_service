import logging
import time

import aiohttp
import jwt
import requests
from fastapi import Depends

from core.config import settings
from db.casher import AbstractCache, get_cacher
from exceptions.errors import UnauthorizedError

logger = logging.getLogger(__name__)


async def verify_token(token: str) -> None:
    """
    Функция отправляет запрос в сервис AUTH для верификации токена
    Args:
        token(str): JWT-токен доступа
    Raises:
        HTTPStatus.UNAUTHORIZED: Если токен недействителен или
        сервис AUTH возвращает ошибку верификации.
    """
    try:
        headers = {"Content-Type": "application/json"}
        json = {"access_token": token}
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=settings.AUTH_SERVICE_URL, headers=headers, json=json
            )
        response.raise_for_status()
    except requests.HTTPError as ex:
        logger.error("HTTPerror: %s", ex)
        raise UnauthorizedError
    except requests.ConnectionError as ex:
        logger.error("Conn error: %s", ex)
        raise UnauthorizedError
    except Exception as ex:
        logger.error("Unexpected error: %s", ex)


async def calc_diff(token: str) -> int:
    """
    Вычисляет разницу между временем истечения токена и текущим временем.
    Args:
        token (str): JWT-токен, из которого будет извлечено время истечения.

    Returns:
        int: Разница в сек между временем истечения токена и текущим временем.
    """
    token_dict: dict = jwt.decode(token, options={"verify_signature": False})
    issue_epoch = int(token_dict.get("exp", 0))
    diff = int(issue_epoch - time.time())
    return diff


class AuthService:
    """
    Сервис для аутентификации пользователей.

    Этот класс отвечает за проверку токенов доступа и
    кэширование результатов проверки.

    Attributes:
        cacher (Cache): Объект кэша, используемый для
        хранения результатов проверки токенов.
    """

    def __init__(
        self,
        cacher: AbstractCache,
    ) -> None:
        self.cacher = cacher

    async def verify(self, token: str) -> None:
        """
        Проверяет действительность токена доступа.

        Если токен уже проверен и результат кэширован,
        метод возвращает без дополнительных проверок.
        В противном случае, токен проверяется, и если он недействителен,
        вызывается исключение UnauthorizedError.

        Args:
            token (str): Токен доступа, который необходимо проверить.

        Raises:
            UnauthorizedError: Если токен недействителен или истек.
        """
        cache_key = f"def verify: {token}"

        is_valid = await self.cacher.get(cache_key)
        if is_valid is not None:
            return

        await verify_token(token)

        diff = await calc_diff(token)
        if diff <= 0:
            raise UnauthorizedError

        await self.cacher.set(cache_key, True, expire=diff)


def get_auth_service(
    cacher: AbstractCache = Depends(get_cacher),
) -> AuthService:
    """
    Функция для создания экземпляра класса AuthService
    """
    return AuthService(
        cacher=cacher,
    )
