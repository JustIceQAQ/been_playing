from typing import Any
from helpers.cache.base import Cache


class NoneCache(Cache):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get(self, key: str) -> Any | None:
        return None

    async def set(self, key: str, value, expire: float = None):
        pass

    async def close(self):
        pass
