import re
from typing import Any

from bs4 import BeautifulSoup

from helpers.parse_helper import ParseInit


class N228MMParse(ParseInit):
    def __init__(self, item: dict[str, Any]):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("title", None)

    def get_date(self, *args, **kwargs) -> str | None:
        top_paragraph: str | None = self.item.get("top_paragraph", None)
        if top_paragraph is None:
            return None
        soup = BeautifulSoup(top_paragraph, "html.parser")
        text = soup.get_text()
        text = re.sub(r"[（(][^）)]*[）)]", "", text)
        date_pattern = re.compile(r"展覽期間[:：]?\s*([^\n]+)", re.IGNORECASE)

        def parse_date(text):
            date_matches = re.findall(r"(\d{4})[年/-](\d{1,2})[月/-](\d{1,2})", text)
            return [
                f"{int(y):04d}-{int(m):02d}-{int(d):02d}" for y, m, d in date_matches
            ]

        period_match = date_pattern.search(text)

        if period_match:
            dates = parse_date(period_match.group(1))
            start_date = dates[0] if len(dates) > 0 else ""
            end_date = dates[1] if len(dates) > 1 else ""
            period = f"{start_date} ~ {end_date}" if end_date else start_date
        else:
            period = None
        return period

    def get_address(self, *args, **kwargs) -> str | None:
        top_paragraph: str | None = self.item.get("top_paragraph", None)
        if top_paragraph is None:
            return None
        soup = BeautifulSoup(top_paragraph, "html.parser")
        text = soup.get_text()
        text = re.sub(r"[（(][^）)]*[）)]", "", text)
        location_pattern = re.compile(
            r"(展覽地點|地點|地址)[:：]?\s*([^\n<]+)", re.IGNORECASE
        )
        location = None
        location_match = location_pattern.search(text)
        if location_match:
            location_raw = location_match.group(2).strip()
            parts = re.split(r"[／/]", location_raw)
            parts = [p.replace("二二八國家紀念館", "").strip() for p in parts]
            location = next(
                (
                    p
                    for p in parts
                    if "樓" in p or "展區" in p or "展示室" in p or "空間" in p
                ),
                "",
            )
            if not location and parts:
                location = parts[-1]
        return location

    def get_figure(self, *args, **kwargs) -> str | None:
        top_image: str | None = self.item.get("topImage", None)
        if top_image is None:
            return None
        filename = top_image.split("v1/")[1].split("/")[0]
        return "https://static.wixstatic.com/media/" + filename

    def get_source_url(self, *args, **kwargs) -> str | None:
        url: str | None = self.item.get("url", None)
        if url is None:
            return None
        return "https://www.228.org.tw" + url
