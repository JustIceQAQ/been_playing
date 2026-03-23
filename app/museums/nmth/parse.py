import bs4

from helpers.parse_helper import ParseInit


class NMTHParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "caption"}).find("span").get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        date_span = self.item.find("span", string="日期")
        if date_span:
            date_text = date_span.next_sibling.strip()
            return date_text

    def get_address(self, *args, **kwargs) -> str | None:
        address_span = self.item.find("span", string="地點")
        if address_span:
            address_text = address_span.next_sibling.strip()
            return address_text

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.nmth.gov.tw/" + self.item.find("a").get("href")
