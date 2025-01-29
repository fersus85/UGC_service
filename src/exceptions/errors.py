class PasswordOrLoginExc(Exception):
    """Ошибка валидации пароли или логина"""


class UnauthorizedExc(Exception):
    """Ошибка аутентификации"""

    def __init__(self, detail: str):
        self.detail = detail


class RoleServiceExc(Exception):
    """Ошибка во время работе Role Service"""


class NoResult(Exception):
    """Данные по запросу не были найдены"""


class UnauthorizedError(Exception):
    """Ошибка авторизации"""


class BadRequestError(Exception):
    """Ошибка в теле запроса"""
