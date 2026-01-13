import bs4

from helpers.parse_helper import ParseInit


class KmoaParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def roc_to_ad(self, date_str: str) -> str:
        y, m, d = map(int, date_str.split("-"))
        return f"{y + 1911:04d}-{m:02d}-{d:02d}"

    def get_title(self, *args, **kwargs) -> str | None:
        title = self.item.find("title").get_text(strip=True)
        return title

    def get_date(self, *args, **kwargs) -> str | None:
        raw_start_date = self.item.find("div", {"title": "檔期時間(起)"})
        if raw_start_date is None:
            return None
        start_span_text = raw_start_date.find("div", {"class": "p"}).get_text(
            strip=True
        )
        start_date = self.roc_to_ad(start_span_text)

        raw_end_date = self.item.find("div", {"title": "檔期時間(訖)"})

        if raw_end_date is None:
            return start_date
        end_span_text = raw_end_date.find("div", {"class": "p"}).get_text(strip=True)
        end_date = self.roc_to_ad(end_span_text)

        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        div = self.item.find("div", {"title": "地點"})
        if div is None:
            return None
        address = div.find("div", {"class": "p"}).get_text(strip=True)
        return address

    def get_figure(self, *args, **kwargs) -> str | None:
        div = self.item.find("div", {"class": "list-pic pic-download"})
        if div is None:
            return None
        lis = div.find_all("li")
        if len(lis) == 0:
            return None

        return lis[0].attrs["data-src"]

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.find("source_url").get_text(strip=True)
