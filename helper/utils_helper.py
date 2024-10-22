import datetime as dt
import zoneinfo

TAIWAN_TIMEZONE = zoneinfo.ZoneInfo("Asia/Taipei")


def date_now() -> dt.date:
    return dt.datetime.now(tz=TAIWAN_TIMEZONE).date()
