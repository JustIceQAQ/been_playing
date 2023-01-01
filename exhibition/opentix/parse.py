import datetime
from typing import Dict

from helper.parse_helper import ParseInit


class OpenTixParse(ParseInit):
    def __init__(self, item: Dict):
        self.item = item.get("source")

    def get_title(self, *args, **kwargs) -> str:
        return self.item.get("title", "")

    def get_date(self, *args, **kwargs) -> str:
        start_date_time = self.item.get("startDateTime", None)
        end_date_time = self.item.get("endDateTime", None)
        date_time_string = ""
        if start_date_time is not None:
            date_time_string += datetime.date.fromtimestamp(
                start_date_time / 1e3
            ).isoformat()

        if end_date_time is not None:
            date_time_string += " ~ "
            date_time_string += datetime.date.fromtimestamp(
                end_date_time / 1e3
            ).isoformat()

        return date_time_string

    def get_address(self, *args, **kwargs) -> str:
        return ", ".join(self.item.get("places", []))

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.get("imageUrl", "")

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return f'{target_domain}{self.item.get("id", "")}'
