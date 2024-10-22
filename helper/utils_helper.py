import datetime as dt
import zoneinfo

TAIWAN_TIMEZONE = zoneinfo.ZoneInfo("Asia/Taipei")


def datetime_now() -> dt.datetime:
    return dt.datetime.now(tz=TAIWAN_TIMEZONE)


def date_now() -> dt.date:
    return datetime_now().date()


def datetime_now_iso_format() -> str:
    return datetime_now().isoformat()
