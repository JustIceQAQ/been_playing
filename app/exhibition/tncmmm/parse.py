import bs4

from helpers.parse_helper import ParseInit


class TncMMMParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("title").strip()

    def get_date(self, *args, **kwargs) -> str | None:
        pass

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://tncmmm.gov.taipei/" + self.item.get("href").strip()
