import abc


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
    async def set(self, key: str, value, expire: float = None):
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self):
        raise NotImplementedError
