import datetime as dt
import zoneinfo
from functools import lru_cache

TAIWAN_TIMEZONE = zoneinfo.ZoneInfo("Asia/Taipei")


def datetime_now() -> dt.datetime:
    return dt.datetime.now(tz=TAIWAN_TIMEZONE)


def date_now() -> dt.date:
    return datetime_now().date()


def datetime_now_iso_format() -> str:
    return datetime_now().isoformat()


@lru_cache
def month_1() -> int:
    return 1 * 30 * 24 * 60 * 60


@lru_cache
def month_3() -> int:
    return month_1() * 3


@lru_cache
def month_6() -> int:
    return month_3() * 2
