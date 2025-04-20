import abc
import datetime
from typing import Any


class Cache(abc.ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @abc.abstractmethod
    async def get(self, key: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def set(
        self,
        key: str,
        value: Any,
        expire: int | str | None = None,
        from_datetime: datetime.datetime | None = None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self):
        raise NotImplementedError
