import bs4

from helper.parse_helper import ParseInit


class NMHParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("p", {"class": "tit"}).get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.find("p", {"class": "time"}).get_text()

    def get_address(self, *args, **kwargs) -> str:
        runtime_address = None
        if address_element := self.item.find("p", {"class": "address"}):
            runtime_address = address_element.get_text()

        return runtime_address

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.find("img").get("src", None)

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.find("a").get("href", None)
