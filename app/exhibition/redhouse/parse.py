import datetime
import re

from helpers.parse_helper import ParseInit


class RedHouseParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item["Title"]

    def get_date(self, *args, **kwargs) -> str | None:
        dates: list | None = self.item.get("dates", None)
        if (dates is None) or (not dates):
            return None
        first_dates: dict = dates[0]

        start_date = first_dates.get("BeginDate", None)
        if start_date is None:
            return None
        ok_start_date = self.re_date_value(start_date)

        end_date = first_dates.get("EndDate", None)
        if end_date is None:
            return ok_start_date

        ok_end_date = self.re_date_value(end_date)

        return ok_start_date + " ~ " + ok_end_date

    def re_date_value(self, start_date: str):
        is_start_date_match = re.search(r"\d+", start_date)
        if is_start_date_match:
            ts_ms = int(is_start_date_match.group(0))
            ts_sec = ts_ms / 1000
            dt = datetime.datetime.fromtimestamp(ts_sec)
            return dt.strftime("%Y-%m-%d")

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item["PlaceName"]

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://www.redhouse.taipei/upload/{}".format(self.item["ListFileName"])

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.redhouse.taipei/eventsCT.aspx?id={}".format(self.item["Id"])
