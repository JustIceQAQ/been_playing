import bs4

from helpers.parse_helper import ParseInit


class N228MMParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.select_one("p span[style='letter-spacing:0em;']").get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        pass

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img").attrs.get("src")

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.select_one("a").attrs.get("href")
