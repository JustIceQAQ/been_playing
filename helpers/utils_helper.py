import datetime as dt
import zoneinfo
from functools import lru_cache

TAIWAN_TIMEZONE = zoneinfo.ZoneInfo("Asia/Taipei")


def datetime_now() -> dt.datetime:
    return dt.datetime.now(tz=TAIWAN_TIMEZONE)


def date_now() -> dt.date:
    return datetime_now().date()


def this_date_year() -> int:
    return date_now().year


def ad_to_roc_era(year: int) -> int:
    return year - 1911


def roc_era_to_ad(roc_era: int) -> int:
    return roc_era + 1911


def datetime_now_iso_format() -> str:
    return datetime_now().isoformat()


def timestamp_to_datetime(timestamp: int) -> dt.datetime:
    return dt.datetime.fromtimestamp(timestamp, tz=TAIWAN_TIMEZONE)


@lru_cache
def month_1() -> int:
    return 1 * 30 * 24 * 60 * 60


@lru_cache
def month_3() -> int:
    return month_1() * 3


@lru_cache
def month_6() -> int:
    return month_3() * 2
