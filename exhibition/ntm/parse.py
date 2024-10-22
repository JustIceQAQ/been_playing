import dataclasses

import bs4

from helper.parse_helper import ParseInit


@dataclasses.dataclass
class PathQuery:
    n: int
    sms: int


class NTMParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("div.caption > span").get_text()

    def get_date(self, *args, **kwargs) -> str:
        if (
            result := self.safe_get_text(self.item.select_one("p.activity-time"))
        ) is not None:
            return result.replace("日期：", "").strip()
        return ""

    def get_address(self, *args, **kwargs) -> str:
        if (
            result := self.safe_get_text(self.item.select_one("p.activity-season"))
        ) is not None:
            return result.replace("地點：", "").strip()
        return ""

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.select_one("img")["src"]

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("a")["href"]
