import bs4

from helper.parse_helper import ParseInit


class KKTixParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one(".event-title").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.select_one("span.date").get_text()

    def get_address(self, *args, **kwargs) -> str:
        return ""

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.select_one("figure > img").get("src")

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("a.cover").get("href")