import bs4

from helpers.parse_helper import ParseInit


class NHRMParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "title"}).get_text().strip()

    def get_date(self, *args, **kwargs) -> str | None:
        date_range = self.item.find("div", {"class": "date"})
        if date_range:
            return (
                date_range.get_text()
                .strip()
                .replace("-", "~")
                .replace("－", "~")
                .replace(".", "-")
            )

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        img = self.item.find("div", {"class": "img"})
        style = img.get("style")
        imager_url = style.split("url(")[1].replace(")", "").replace("'", "")
        return imager_url

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.find("a", {"class": "more"}).get("href")
