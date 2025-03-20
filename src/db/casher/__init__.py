from typing import Any, Optional, Protocol


class AbstractCache(Protocol):
    """Абстрактый класс для кэша"""

    async def set(
            self,
            key: str,
            value: Any,
            expire: Optional[int] = None,
            raise_exc: bool = False
    ) -> None:
        pass

    async def get(self, key: str, raise_exc: bool = False) -> Optional[Any]:
        pass

    async def incr(
            self,
            key: str,
            value: int,
            raise_exc: bool = False
    ) -> int:
        pass


# cacher = Optional[AbstractCache]
cacher: Optional[AbstractCache] = None


async def get_cacher() -> AbstractCache | None:
    return cacher
