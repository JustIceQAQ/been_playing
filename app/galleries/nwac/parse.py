from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class NWACParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.css_first("img").attributes.get("alt")

    def get_date(self, *args, **kwargs) -> str | None:
        pass

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.css_first("img").attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.css_first("a").attributes.get("href")
