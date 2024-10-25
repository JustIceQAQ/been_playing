import asyncio
import functools
import pathlib
from typing import Any

from diskcache import Cache


class DiskCache:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.cache = Cache(
            str(
                pathlib.Path(__file__).parent.parent.parent.parent.absolute()
                / "fixture"
            )
        )
        self.loop = asyncio.get_running_loop()

    async def get(self, key: str) -> Any | None:
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(None, self.cache.get, key)
        result = await future
        return result

    async def set(self, key: str, value, expire: float = None):
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(
            None, functools.partial(self.cache.set, key, value, expire=expire)
        )
        result = await future
        return result

    async def close(self):
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(
            None,
            self.cache.close,
        )
        await future
