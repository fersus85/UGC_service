from fastapi import Query


class PaginateQueryParams:
    """
    Класс для разделения ответов на страницы.
    """

    def __init__(
        self,
        page_number: int = Query(
            1,
            title="Page number.",
            description="Номер страницы (начиная с 1)",
            ge=1,
        ),
        page_size: int = Query(
            50,
            title="Page size.",
            description="Количество записей на странице (от 1 до 100)",
            ge=1,
            le=100,
        ),
    ):
        """
        Инициализирует класс пагинации ответов.
        """
        self.page_number = page_number
        self.page_size = page_size
