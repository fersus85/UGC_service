import jwt
from fastapi import Depends, Request

from exceptions.errors import UnauthorizedExc


def get_access_token_from_cookies(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise UnauthorizedExc("Access token not found")

    return token


async def get_user_id_from_access_token(
    access_token: str = Depends(get_access_token_from_cookies),
):
    try:
        payload = jwt.decode(
            access_token,
            options={"verify_signature": False},
        )
    except jwt.InvalidTokenError:
        raise UnauthorizedExc("Token is invalid")

    user_id = payload.get("user_id")
    if not user_id:
        raise UnauthorizedExc("User ID not found")

    return user_id
