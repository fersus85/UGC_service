import jwt
from fastapi import Depends, Request

from exceptions.errors import UnauthorizedExc
from services.auth_service import AuthService, get_auth_service


def get_access_token_from_cookies(request: Request) -> str:
    """
    Извлекает Access токен из Cookies
    """
    token = request.cookies.get("access_token")

    if not token:
        raise UnauthorizedExc("Access token not found")

    return token


async def get_user_id_from_access_token(
    access_token: str = Depends(get_access_token_from_cookies),
    auth_service: AuthService = Depends(get_auth_service),
) -> str:
    """
    Извлекает user_id из Access токена
    и проверяет валидность токена через Auth Service
    """
    try:
        payload: dict = jwt.decode(
            access_token,
            options={"verify_signature": False},
        )
    except jwt.InvalidTokenError:
        raise UnauthorizedExc("Token is invalid")

    await auth_service.verify(access_token)

    user_id = payload.get("user_id")
    if not user_id:
        raise UnauthorizedExc("User ID not found")

    return user_id
