import bs4
import datetime
from helpers.parse_helper import ParseInit


class YiYunParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h3", {"class": "big-title"}).get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        dates_text = self.item.select("div.date-text")
        start_date, end_date = dates_text
        start_date_text = datetime.datetime.strptime(start_date.get_text(strip=True), "%m/%d/%Y").strftime("%Y-%m-%d")
        end_date_text = datetime.datetime.strptime(end_date.get_text(strip=True), "%m/%d/%Y").strftime("%Y-%m-%d")
        return f"{start_date_text} ~ {end_date_text}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        if self.item.name == "a":
            return "https://www.yiyun-art.com" + self.item.get("href")
        return "https://www.yiyun-art.com" + self.item.find("a").get("href")
