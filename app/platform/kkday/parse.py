import bs4

from helpers.parse_helper import ParseInit


class KKDayParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("name")

    def get_date(self, *args, **kwargs) -> str | None:
        return ""

    def get_address(self, *args, **kwargs) -> str | None:
        return ""

    def get_figure(self, *args, **kwargs) -> str | None:
        img_url = self.item.get("img_url", None)
        if img_url:
            return img_url
        img_url_list = self.item.get("img_url_list", None)
        if img_url_list:
            return img_url_list[0]

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.get("url")
