import datetime

import bs4

from helpers.parse_helper import ParseInit


class ShungYeArtParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.select_one("div.fig > h4").text.strip()

    def get_date(self, *args, **kwargs) -> str | None:
        raw_date = self.item.select_one("div.fig > p").text.strip()
        if "持續" in raw_date:
            return None

        start_str, end_str = raw_date.split(" - ")
        start_date = datetime.datetime.strptime(start_str, "%Y.%m.%d").strftime(
            "%Y-%m-%d"
        )
        end_date = datetime.datetime.strptime(end_str, "%Y.%m.%d").strftime("%Y-%m-%d")

        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        result = self.item.select_one("a > div.info2")
        if result is None:
            return None
        style = result.get("style").split("background: url(")[1].split(");")[0]
        return "https://www.shungye-art.org/" + style

    def get_source_url(self, *args, **kwargs) -> str | None:
        return (
            "https://www.shungye-art.org/"
            + self.item.find("a").attrs["href"].split("&")[0]
        )
