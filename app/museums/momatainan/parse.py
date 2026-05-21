import re

from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class MoMaTainanParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.attributes.get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        p = self.item.css_first("div.p p").text(strip=True)
        if "日期｜" in p:
            raw_date = p.split("日期｜")[1].split("&")[0].split("／")[0].split("\xa0")[0]
            match = re.search(r"(\d+)年(\d+)月(\d+)日至(\d+)年(\d+)月(\d+)日", raw_date)
            if match is None:
                return None
            ry1, m1, d1, ry2, m2, d2 = (int(x) for x in match.groups())
            start = f"{ry1}-{m1:02d}-{d1:02d}"
            end = f"{ry2}-{m2:02d}-{d2:02d}"
            return f"{start} ~ {end}"

    def get_address(self, *args, **kwargs) -> str | None:
        p = self.item.css_first("div.p p").text(strip=True)
        if "地點｜" in p:
            raw_address = (
                p.split("地點｜")[1].split("&")[0].split("／")[0].split("\xa0")[0].replace("臺南國家美術館", "")
            )
            return raw_address

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.css_first("img").attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.momatainan.gov.tw/" + self.item.attributes.get("href")
