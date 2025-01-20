from typing import Any, Callable, Coroutine

from fastapi import Request, Response

from exceptions import errors
from exceptions.exc_handlers import (
    no_result_error_400_handler,
    password_or_login_error_handler,
    role_service_error_handler,
    unauthorized_error_handler,
)

exception_handlers: dict[
    int | type[Exception],
    Callable[[Request, errors.UnauthorizedExc], Coroutine[Any, Any, Response]],
] = {
    errors.PasswordOrLoginExc: password_or_login_error_handler,
    errors.UnauthorizedExc: unauthorized_error_handler,
    errors.NoResult: no_result_error_400_handler,
    errors.RoleServiceExc: role_service_error_handler,
}
