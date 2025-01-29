from typing import Any, Optional, Protocol


class AbstractCache(Protocol):
    """Абстрактый класс для кэша"""

    async def set(self, key: str, value: Any, expire: int) -> None:
        pass

    async def get(self, key: str) -> Optional[Any]:
        pass


# cacher = Optional[AbstractCache]
cacher: Optional[AbstractCache] = None


async def get_cacher() -> AbstractCache | None:
    return cacher
