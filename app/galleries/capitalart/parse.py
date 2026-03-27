import bs4

from helpers.parse_helper import ParseInit


class CapitalArtParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        a = self.item.find("h3", {"class": "title"}).find("a")
        return a.get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        date = self.item.find("div", {"class": "date"}).get_text(strip=True)
        date_str = date.split("：")[1].strip()
        return date_str.replace("-", "~").replace(".", "-")

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        style = self.item.find("div", {"class": "pic"}).get("style")
        return "https://capitalart.com.tw" + style.split("url(")[1][:-2]

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        a = self.item.find("h3", {"class": "title"}).find("a")
        return "https://capitalart.com.tw" + a.get("href")
