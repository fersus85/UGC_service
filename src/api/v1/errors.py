from fastapi import APIRouter

# error demonstration
router = APIRouter(
    prefix="/error",
    tags=["Error"],
)


@router.get(
    "/",
    summary="Ошибка деления на ноль",
    description="Демонстрация ошибки деления на ноль",
)
async def get_film_bookmarks() -> None:
    1 / 0  # noqa: WPS344
    return None
