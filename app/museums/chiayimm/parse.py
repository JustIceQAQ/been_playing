import bs4

from helpers.parse_helper import ParseInit


def convert_roc_range_to_iso(date_range_str):
    parts = date_range_str.split(" ~ ")
    converted_dates = []
    for part in parts:
        y, m, d = part.strip().split("/")
        western_year = int(y) + 1911
        formatted_date = f"{western_year}-{int(m):02d}-{int(d):02d}"
        converted_dates.append(formatted_date)
    return " ~ ".join(converted_dates)


class ChiayiMMParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "kf-title"}).get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        ps = self.item.select("div.kf-date p")
        if not ps:
            return None
        for p in ps:
            text = p.get_text(strip=True)
            if "時間" in text:
                raw_date = text.split(":")[-1]
                return convert_roc_range_to_iso(raw_date)

    def get_address(self, *args, **kwargs) -> str | None:
        ps = self.item.select("div.kf-date p")
        if not ps:
            return None
        for p in ps:
            text = p.get_text(strip=True)
            if "地點" in text:
                raw_address = text.split(":")[-1]
                return raw_address

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://museum.chiayi.gov.tw/" + self.item.find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://museum.chiayi.gov.tw/" + self.item.get("href")
