class PasswordOrLoginExc(Exception):
    """Ошибка валидации пароли или логина"""

    pass


class UnauthorizedExc(Exception):
    """Ошибка аутентификации"""

    def __init__(self, detail: str):
        self.detail = detail


class RoleServiceExc(Exception):
    """Ошибка во время работе Role Service"""

    pass


class NoResult(Exception):
    """Данные по запросу не были найдены"""

    pass


class UnauthorizedError(Exception):
    """Ошибка авторизации"""

    pass


class BadRequestError(Exception):
    """Ошибка в теле запроса"""

    pass
