import bs4

from helpers.parse_helper import ParseInit


class TnCsEcParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "caption"}).get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        date = self.item.find("p", {"class": "activity-time"}).get_text(strip=True)
        return date.replace("日期：", "")

    def get_address(self, *args, **kwargs) -> str | None:
        address = self.item.find("p", {"class": "activity-season"}).get_text(strip=True)
        return address.replace("地點：", "")

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.get("href")
