import bs4

from helper.parse_helper import ParseInit


class NTSECParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("div", {"class": "newsMessage-content"}).get_text()

    def get_date(self, *args, **kwargs) -> str:
        return "-"

    def get_address(self, *args, **kwargs) -> str:
        return "-"

    def get_figure(self, *args, **kwargs) -> str:
        return has_img.get("src") if (has_img := self.item.find("img")) else "-"

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.get("href")
