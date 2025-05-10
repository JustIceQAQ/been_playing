import bs4

from helpers.parse_helper import ParseInit


class KdMoFaParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return (
            self.item.find("div", {"class": "cont"})
            .find("div", {"class": "STitle"})
            .text
        )

    def get_date(self, *args, **kwargs) -> str | None:
        datetime_range = (
            self.item.find("div", {"class": "cont"}).find("div", {"class": "subt"}).text
        )
        return datetime_range.replace(".", "-").replace("～", " ~ ")

    def get_address(self, *args, **kwargs) -> str | None:
        return (
            self.item.find("div", {"class": "cont"})
            .find("div", {"class": "location"})
            .text
        )

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "pic"}).find("img").get("src")

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.get("href")
