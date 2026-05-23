import re

from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit
from helpers.utils_helper import to_ad_year, set_date


class AfmcParse(ParseInit):
    BASE_URL = "https://www.afmc.gov.tw"

    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.attributes.get("title")

    def _parse_roc_date(self, date_str: str) -> str | None:
        cleaned = re.sub(r"\s*\([^)]+\)", "", date_str).strip()
        parts = cleaned.split(".")
        if len(parts) != 3:
            return None
        try:
            ad_year = to_ad_year(int(parts[0]))
            return set_date(ad_year, int(parts[1]), int(parts[2])).isoformat()
        except (ValueError, TypeError):
            return None

    def get_date(self, *args, **kwargs) -> str | None:
        p = self.item.css_first("p.data")
        if p is None:
            return None
        date_text = p.text(strip=True)
        if "~" in date_text:
            parts = date_text.split("~", 1)
            start = self._parse_roc_date(parts[0]) if parts[0].strip() else None
            end = self._parse_roc_date(parts[1]) if parts[1].strip() else None
            if start and end:
                return f"{start} ~ {end}"
            elif start:
                return f"{start} ~"
            elif end:
                return f"~ {end}"
            return None
        return self._parse_roc_date(date_text)

    def get_address(self, *args, **kwargs) -> str | None:
        p = self.item.css_first("p.where")
        if p is None:
            return None
        return p.text(strip=True)

    def get_figure(self, *args, **kwargs) -> str | None:
        img = self.item.css_first("img")
        if img is None:
            return None
        src = img.attributes.get("src")
        if not src:
            return None
        if src.startswith("http"):
            return src
        return self.BASE_URL + src

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        p = self.item.css_first("p.dtype")
        if p is None:
            return None
        tag = p.text(strip=True)
        return [tag] if tag else None

    def get_source_url(self, *args, **kwargs) -> str | None:
        href = self.item.attributes.get("href")
        if not href:
            return None
        path = href.split("?")[0]
        return self.BASE_URL + path
