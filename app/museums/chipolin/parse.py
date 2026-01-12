import bs4

from helpers.parse_helper import ParseInit


class ChiPoLinParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        h2 = self.item.find("h2", {"class": "exhibition__item__title"})
        for span in h2.find_all("span"):
            span.extract()
        text = h2.get_text(strip=True)
        return text

    def get_date(self, *args, **kwargs) -> str | None:
        span = self.item.find(
            "span", {"class": "exhibition__item__title__date"}
        ).get_text()
        return span.replace("-", "~").replace("/", "-")

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        style = self.item.find("div", {"class": "exhibition__item__img"}).get("style")
        img = style.split("url(")[1][:-1]
        return img

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.find("a", {"class": "click-range"}).get("href")
