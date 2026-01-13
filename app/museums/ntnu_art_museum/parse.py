import bs4

from helpers.parse_helper import ParseInit


class NTNUArtMuseumParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("figcaption").get_text().strip()

    def get_date(self, *args, **kwargs) -> str | None:
        pass

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img").get("src")

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.find("a").get("href")
