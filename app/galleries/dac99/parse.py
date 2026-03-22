import bs4

from helpers.parse_helper import ParseInit


class Dac99Parse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h3", {"class": "exhibition-current__name"}).get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        date = self.item.find("p", {"class": "exhibition-current__date"}).get_text(strip=True)
        return date.replace("─", "~").replace(".", "-")

    def get_address(self, *args, **kwargs) -> str | None:
        exhibition_current__text = self.item.find("p", {"class": "exhibition-current__text"}).get_text(strip=True)
        return exhibition_current__text.split("展覽地點：")[1].split("（")[0].strip()

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://99dac.com/" + self.item.find("img").get("src")[2:]

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        href = self.item.find("a", {"class": "exhibition-current__btn-detail"}).get("href")
        return "https://99dac.com/" + href
