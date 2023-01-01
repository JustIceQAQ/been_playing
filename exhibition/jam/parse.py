import bs4

from helper.parse_helper import ParseInit


class JamParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("h3", {"class": "field-content"}).get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.find("div", {"class": "event-date"}).get_text()

    def get_address(self, *args, **kwargs) -> str:
        return "-"

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.find("img", {"class": "image-style-event-list"}).get("src")

    def get_source_url(self, *args, **kwargs) -> str:
        return "http://jam.jutfoundation.org.tw{}".format(
            self.item.find("h3", {"class": "field-content"}).find("a").get("href")
        )
