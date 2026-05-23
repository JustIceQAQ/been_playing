import re
from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class ELandAMParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        raw_title = self.item.attributes.get("title")
        if raw_title is None:
            return None

        return raw_title.split("】")[1].strip()

    def get_date(self, *args, **kwargs) -> str | None:
        raw_date = self.item.attributes.get("title")
        if raw_date is None:
            return None

        match = re.search(r"【(\d+)年(\d+)月(\d+)日[~～](\d+)年(\d+)月(\d+)日】", raw_date)
        if match is None:
            return None

        ry1, m1, d1, ry2, m2, d2 = (int(x) for x in match.groups())
        start = f"{ry1 + 1911}-{m1:02d}-{d1:02d}"
        end = f"{ry2 + 1911}-{m2:02d}-{d2:02d}"
        return f"{start} ~ {end}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.css_first("img").attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://ymoa.e-land.gov.tw/" + self.item.attributes.get("href")
