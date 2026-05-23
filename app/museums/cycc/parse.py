from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit

BASE_URL = "https://cycc.org.tw"


class CyccParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        a = self.item.css_first("h3 a")
        return a.text(strip=True) if a else None

    def get_date(self, *args, **kwargs) -> str | None:
        date_divs = self.item.css("div.recent-date")
        if not date_divs:
            return None

        def _extract(div) -> str | None:
            span = div.css_first("span[content]")
            if span is None:
                return None
            content = span.attributes.get("content", "")
            return content[:10] if len(content) >= 10 else None

        if len(date_divs) >= 2:
            start = _extract(date_divs[0])
            end = _extract(date_divs[1])
            if start and end:
                return f"{start} ~ {end}"
            if start:
                return f"{start} ~"
            if end:
                return f"~ {end}"
        elif len(date_divs) == 1:
            return _extract(date_divs[0])
        return None

    def get_address(self, *args, **kwargs) -> str | None:
        return None

    def get_figure(self, *args, **kwargs) -> str | None:
        img = self.item.css_first("img")
        if img is None:
            return None
        src = img.attributes.get("src", "")
        if not src:
            return None
        return src if src.startswith("http") else BASE_URL + src

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        return None

    def get_source_url(self, *args, **kwargs) -> str | None:
        a = self.item.css_first("h3 a")
        if a is None:
            return None
        href = a.attributes.get("href", "")
        if not href:
            return None
        return href if href.startswith("http") else BASE_URL + href
