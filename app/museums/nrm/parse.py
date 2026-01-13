import bs4

from helpers.parse_helper import ParseInit


class NrmParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("title").replace("[另開新視窗]", "").strip()

    def get_date(self, *args, **kwargs) -> str | None:
        return (
            self.item.find("p", {"class": "activity-time"})
            .get_text()
            .replace("日期：", "")
        )

    def get_address(self, *args, **kwargs) -> str | None:
        address_result = self.item.find("p", {"class": "activity-season"})
        if address_result:
            return address_result.get_text().replace("地點：", "")

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "img"}).find("img").get("src")

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.get("href")
