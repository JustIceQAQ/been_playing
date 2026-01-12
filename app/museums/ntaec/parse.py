import bs4

from helpers.parse_helper import ParseInit


class NTAECParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def roc_to_ad(self, date_str: str) -> str:
        y, m, d = map(int, date_str.split("-"))
        return f"{y + 1911:04d}-{m:02d}-{d:02d}"

    def get_title(self, *args, **kwargs) -> str | None:
        a = self.item.select_one("h2.title > a")
        return a.get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        i = self.item.find("i", {"class": "fa-clock-o"})
        if i is None:
            return None
        date_string = i.next_sibling.strip()
        date_range = date_string.split("~")
        if len(date_range) == 1:
            return self.roc_to_ad(date_range[0])
        if len(date_range) == 2:
            start, end = date_range
            start_date = self.roc_to_ad(start)
            end_date = self.roc_to_ad(end)
            return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        i = self.item.find("i", {"class": "fa-map-marker"})
        if i is None:
            return None
        data = i.next_sibling.strip()
        return data

    def get_figure(self, *args, **kwargs) -> str | None:
        div = self.item.find("div", {"class": "image-block"})
        if div is None:
            return None
        style = div.get("style")
        data = style.split(":url(")[1]
        return data[:-2]

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        a = self.item.select_one("h2.title > a")
        return "https://www.arte.gov.tw/" + a.attrs["href"]
