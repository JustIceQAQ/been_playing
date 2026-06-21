import asyncio
import datetime
import functools
import pathlib
from typing import Any
from croniter import croniter
from diskcache import Cache as package_disk_cache

from helpers.cache.base import CacheBase
from zoneinfo import ZoneInfo


class DiskCache(CacheBase):
    _instance = None
    _zoneinfo = ZoneInfo("Asia/Taipei")

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.origin_cache = package_disk_cache(
            str(pathlib.Path(__file__).parent.parent.parent.parent.absolute() / "fixture")
        )

    @property
    def loop(self):
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.get_event_loop()

    def _get_datetime_now(self):
        return datetime.datetime.now(tz=self._zoneinfo)

    def get(self, key: str) -> Any | None:
        return self.origin_cache.get(key)

    async def aget(self, key: str) -> Any | None:
        future = self.loop.run_in_executor(None, self.get, key)
        result = await future
        return result

    async def aset(
        self,
        key: str,
        value: Any,
        expire: int | str | None = None,
        from_datetime: datetime.datetime | None = None,
    ) -> bool | None:
        future = self.loop.run_in_executor(
            None,
            functools.partial(self.set, key, value, expire=expire, from_datetime=from_datetime),
        )
        result = await future
        return result

    def set(
        self,
        key: str,
        value: Any,
        expire: int | str | None = None,
        from_datetime: datetime.datetime | None = None,
    ):
        expire_seconds = self.get_expire_seconds(expire, from_datetime)
        return self.origin_cache.set(key, value, expire=expire_seconds)

    def get_expire_seconds(self, expire, from_datetime):
        if isinstance(expire, str) and croniter.is_valid(expire):
            expire_seconds = self.croniter_str_to_seconds(expire, from_datetime)
        elif isinstance(expire, int):
            expire_seconds = expire
        else:
            expire_seconds = None
        return expire_seconds

    def croniter_str_to_seconds(self, croniter_string: str, from_datetime: datetime.datetime | None = None) -> int:
        runtime_now = self._get_datetime_now()
        croniter_iter = croniter(croniter_string, (from_datetime or runtime_now))
        next_time: datetime.datetime = croniter_iter.get_next(datetime.datetime)
        return (next_time - (from_datetime or runtime_now)).seconds

    async def close(self):
        future = self.loop.run_in_executor(
            None,
            self.origin_cache.close,
        )
        await future


disk_cache = DiskCache()
