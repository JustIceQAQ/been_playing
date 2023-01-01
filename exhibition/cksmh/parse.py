import bs4

from helper.parse_helper import ParseInit


class CKSMHParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a > div.h3").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > span.date").get_text().replace("/", "-")

    def get_address(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > span.location").get_text()

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a > span > img")["src"]

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a")["href"]
