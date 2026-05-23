import bs4

from helpers.parse_helper import ParseInit


class ChCsEcParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "caption"}).find("span").get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        date = self.item.find("p", {"class": "activity-time"})
        if date:
            return date.get_text(strip=True).replace("日期：", "")

    def get_address(self, *args, **kwargs) -> str | None:
        address = self.item.find("p", {"class": "activity-season"})
        if address:
            return address.get_text(strip=True).replace("地點：", "").replace("國立彰化生活美學館", "").strip()

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.get("href")
