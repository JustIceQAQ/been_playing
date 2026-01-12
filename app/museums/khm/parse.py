import bs4

from helpers.parse_helper import ParseInit


class KhmParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h3", {"class": "item-title"}).get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        return (
            self.item.find("span", {"class": "item-date"})
            .get_text(strip=True)
            .replace(".", "-")
        )

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        style = self.item.find("div", {"class": "background-img"}).get("style")
        url = style.split("url(")[1][:-2]
        return url

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.find("a", {"class": "list-link"}).get("href")
