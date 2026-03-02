import datetime as dt
import zoneinfo
from functools import lru_cache
from dateutil.relativedelta import relativedelta
from aiolimiter import AsyncLimiter

TAIWAN_TIMEZONE = zoneinfo.ZoneInfo("Asia/Taipei")


def get_timezone():
    return TAIWAN_TIMEZONE


def get_timezone_str():
    return TAIWAN_TIMEZONE.key


def get_datetime_now() -> dt.datetime:
    return dt.datetime.now(tz=TAIWAN_TIMEZONE)


def get_date_now() -> dt.date:
    return get_datetime_now().date()


def get_date_format_digit() -> str:
    # YYYYMMDD
    this_date = get_datetime_now().date()
    return this_date.strftime("%Y%m%d")


def get_this_date_year() -> int:
    return get_date_now().year


def get_ad_to_roc_era(year: int) -> int:
    return year - 1911


def get_roc_era_to_ad(roc_era: int) -> int:
    return roc_era + 1911


def get_datetime_now_iso_format() -> str:
    return get_datetime_now().isoformat()


def timestamp_to_datetime(timestamp: int) -> dt.datetime:
    return dt.datetime.fromtimestamp(timestamp, tz=TAIWAN_TIMEZONE)


def get_current_and_previous_month():
    now = get_datetime_now()

    current_period = (now.year, now.month)

    last_month_date = now - relativedelta(months=1)
    previous_period = (last_month_date.year, last_month_date.month)

    return current_period, previous_period


@lru_cache
def month_1() -> int:
    return 1 * 30 * 24 * 60 * 60


@lru_cache
def month_3() -> int:
    return month_1() * 3


@lru_cache
def month_6() -> int:
    return month_3() * 2


def get_asyncio_rate_limit(concurrent: int, second: int) -> AsyncLimiter:
    return AsyncLimiter(concurrent, second)


if __name__ == "__main__":
    print(get_date_format_digit())
