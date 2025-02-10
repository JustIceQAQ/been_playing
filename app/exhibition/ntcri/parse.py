import bs4

from helpers.parse_helper import ParseInit
from helpers.utils_helper import timestamp_to_datetime


class NTCRIParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("name")

    def get_date(self, *args, **kwargs) -> str | None:
        start_date, end_date = None, None
        if start_date_timestamp := self.item.get("startDate", None):
            start_date = timestamp_to_datetime(int(str(start_date_timestamp)[:-3]))
        if end_date_timestamp := self.item.get("endDate", None):
            end_date = timestamp_to_datetime(int(str(end_date_timestamp)[:-3]))
        if start_date is None:
            return None
        this_date = start_date.strftime("%Y-%m-%d")
        if end_date is None:
            return this_date
        this_date += f" ~ {end_date.strftime('%Y-%m-%d')}"
        return this_date

    def get_address(self, *args, **kwargs) -> str | None:
        performances: list[dict[str, str]] = self.item.get("performances")
        return performances[0].get("perfName")

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.get("image").get("original")

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.get("actUrl")
