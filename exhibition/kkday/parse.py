from typing import Dict

from helper.parse_helper import ParseInit


class KKDayParse(ParseInit):
    def __init__(self, item: Dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.get("name")

    def get_date(self, *args, **kwargs) -> str:
        return ""

    def get_address(self, *args, **kwargs) -> str:
        return ""

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.get("img_url")

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.get("url")
