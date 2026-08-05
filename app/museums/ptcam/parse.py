import re

from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class PTCAMParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        content = self.item.css_first("meta[property='og:title']").attributes.get("content")
        return content.split("（")[0].split("(")[0].strip()

    def get_date(self, *args, **kwargs) -> str | None:
        content = self.item.css_first("meta[property='og:title']").attributes.get("content")

        # Case 1: 日期直接在 title 內，如 (2026.03.28-2026.08.30)
        match = re.search(r"\((\d{4})\.(\d{1,2})\.(\d{1,2})-(\d{4})\.(\d{1,2})\.(\d{1,2})\)", content)
        if match:
            start = f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"
            end = f"{match.group(4)}-{int(match.group(5)):02d}-{int(match.group(6)):02d}"
            return f"{start} ~ {end}"

        # Case 2: title 無日期（如臺語名），從內文 展期｜ 抓
        content_div = self.item.css_first("#ContentPlaceHolder1_divContent")
        if content_div is None:
            return None
        for p in content_div.css("p"):
            text = p.text().strip()
            if "展期｜" not in text:
                continue
            match = re.search(r"展期｜(\d{4})\.(\d{1,2})\.(\d{1,2})\s*[–—-]\s*(\d{4})\.(\d{1,2})\.(\d{1,2})", text)
            if match:
                start = f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"
                end = f"{match.group(4)}-{int(match.group(5)):02d}-{int(match.group(6)):02d}"
                return f"{start} ~ {end}"

        return None

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.css_first("meta[property='og:image']").attributes.get("content")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.css_first("meta[property='og:url']").attributes.get("content")
