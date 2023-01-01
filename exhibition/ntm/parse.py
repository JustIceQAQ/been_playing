import bs4

from helper.parse_helper import ParseInit


class NTMParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > h2 > a").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return "".join(
            [
                label.get_text().strip()
                for label in self.item.select("dd > ul > li:nth-child(1) > label")
            ]
        ).replace("/", "-")

    def get_address(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > ul > li:nth-child(2)").get_text()

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a")["href"]

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > h2 > a")["href"]
