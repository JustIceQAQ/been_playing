import datetime
import datetime as dt
import zoneinfo
from functools import lru_cache

from aiolimiter import AsyncLimiter
from dateutil.relativedelta import relativedelta

TAIWAN_TIMEZONE = zoneinfo.ZoneInfo("Asia/Taipei")


class GetDate:
    """當前時間工具，以台灣時區為基準"""

    def __init__(self):
        self._timezone = TAIWAN_TIMEZONE
        self._now = dt.datetime.now(tz=self._timezone)

    @property
    def timezone(self) -> zoneinfo.ZoneInfo:
        return self._timezone

    @property
    def timezone_string(self) -> str:
        return self._timezone.key

    @property
    def time_now(self) -> dt.datetime:
        return dt.datetime.now(tz=TAIWAN_TIMEZONE)

    @property
    def time_now_format_to_ios(self) -> str:
        return self.time_now.isoformat()

    @property
    def now(self) -> dt.date:
        return self.time_now.date()

    @property
    def now_format_to_digit(self) -> str:
        """format to YYYYMMDD"""
        return self.now.strftime("%Y%m%d")

    @property
    def now_format_to_ios(self) -> str:
        """format to YYYY-MM-DD"""
        return self.now.strftime("%Y-%m-%d")

    @property
    def now_year(self) -> int:
        return self.now.year

    @property
    def now_year_format_to_roc_era(self) -> int:
        return self.now.year - 1911

    @property
    def now_format_to_roc_era_ios(self) -> str:
        """format to [ROC YEAR]-MM-DD"""
        this_date = self.now
        roc_era = this_date.year - 1911
        return f"{roc_era}-{this_date.month:02d}-{this_date.day:02d}"

    @property
    def now_format_to_timestamp(self) -> int:
        return int(self.time_now.timestamp() * 1000)

    @property
    def current_and_previous_period(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """回傳當前與上個月的年月 ((YYYY, MM), (YYYY, MM))

        Returns:
            like
                ((2026, 5), (2026, 4))
                or
                ((2026, 1), (2025, 12))
        """
        now = self.time_now
        current_period = (now.year, now.month)
        last_month_date = now - relativedelta(months=1)
        previous_period = (last_month_date.year, last_month_date.month)
        return current_period, previous_period


get_date = GetDate()


def to_roc_era_year(year: int) -> int:
    return year - 1911


def to_ad_year(roc_era: int) -> int:
    return roc_era + 1911


def timestamp_to_datetime(timestamp: int) -> dt.datetime:
    return dt.datetime.fromtimestamp(timestamp, tz=TAIWAN_TIMEZONE)


def set_date(year: int, month: int, day: int) -> datetime.date:
    return dt.date(year, month, day)


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
