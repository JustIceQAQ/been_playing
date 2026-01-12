import bs4

from helpers.parse_helper import ParseInit


class KmFaParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h4", {"class": "exhibition_title"}).get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        data_range = self.item.find("span", {"class": "exhibition_date"}).get_text(
            strip=True
        )
        return data_range.replace("-", "~").replace(".", "-")

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        path = self.item.find("img").attrs["src"]
        return "https://www.kmfa.gov.tw/" + path

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        path = self.item.attrs["href"]
        return "https://www.kmfa.gov.tw" + path
