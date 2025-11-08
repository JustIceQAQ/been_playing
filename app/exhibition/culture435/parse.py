import bs4

from app.exhibition.culture435.utils import parse_range_with_location
from helpers.parse_helper import ParseInit


class Culture435Parse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.select_one("a").attrs["title"]

    def get_date(self, *args, **kwargs) -> str | None:
        desc = self.item.find("div", {"class": "desc"}).get_text(strip=True)
        date_range = parse_range_with_location(desc)
        return date_range

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.select_one("div.img > img").attrs["src"]

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return (
            "https://www.435.culture.ntpc.gov.tw"
            + self.item.select_one("a").attrs["href"]
        )
