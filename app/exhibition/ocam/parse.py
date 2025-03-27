from typing import Any

from helpers.parse_helper import ParseInit


class OCAMParse(ParseInit):
    def __init__(self, item: dict[str, Any] | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item["subject"]

    def get_date(self, *args, **kwargs) -> str | None:
        begin_time = self.item["begtime"]
        end_time = self.item["endtime"]
        return f"{begin_time} ~ {end_time}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://www.ocam.org.tw" + self.item["src"]

    def get_source_url(self, *args, **kwargs) -> str | None:
        id = self.item["id"]
        return f"https://www.ocam.org.tw/tw/Exhibition/ExhibitionDetail/OCAM/{id}"
