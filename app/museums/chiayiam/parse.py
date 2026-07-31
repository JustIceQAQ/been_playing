import bs4

from helpers.parse_helper import ParseInit


class ChiayiAMParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        title = self.item.attrs.get("title")
        if title:
            return title
        return None

    def get_date(self, *args, **kwargs) -> str | None:
        spans = self.item.select("div.date span")
        if not spans:
            return None
        return " ~ ".join([span.get_text(strip=True).replace("-", "").replace("／", "-") for span in spans])

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "place"}).find("span").get_text(strip=True)

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://chiayiartmuseum.chiayi.gov.tw/" + self.item.get("href")
