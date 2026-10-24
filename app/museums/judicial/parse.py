from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class JudicialParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.css_first("div.title").text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        time_element = self.item.css_first("time").text(strip=True)
        parts = time_element.split(" 至 ")
        if len(parts) != 2:
            return None

        formatted_dates = []
        for part in parts:
            y, m, d = part.split("-")
            west_year = int(y) + 1911
            formatted_dates.append(f"{west_year}-{m}-{d}")

        return " ~ ".join(formatted_dates)

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        src = self.item.css_first("img").attrs.get("src")
        return "https://www.judicial.gov.tw" + src

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        href = self.item.attrs.get("href")
        return "https://www.judicial.gov.tw" + href
