import re

from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class PT1936Parse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        content = self.item.css_first("meta[property='og:title']").attributes.get("content")
        return content.split("（")[0].split("(")[0].strip()

    def get_date(self, *args, **kwargs) -> str | None:
        content = self.item.css_first("meta[property='og:title']").attributes.get("content")
        if "常設展" in content:
            return None
        match = re.search(r"\((\d{4})\.(\d{1,2})\.(\d{1,2})-(\d{4})\.(\d{1,2})\.(\d{1,2})\)", content)
        if not match:
            return None
        start = f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"
        end = f"{match.group(4)}-{int(match.group(5)):02d}-{int(match.group(6)):02d}"
        return f"{start} ~ {end}"

    def get_address(self, *args, **kwargs) -> str | None:
        content_div = self.item.css_first("#ContentPlaceHolder1_divContent")
        if content_div is None:
            return None

        paragraphs = [p.text().strip() for p in content_div.css("p")]

        # 優先：展區｜（Case 4）
        for text in paragraphs:
            if "展區｜" in text:
                return text.split("展區｜", 1)[1].strip()

        # 次要：地點｜ / 展覽地點｜（Cases 1, 2, 3）
        for text in paragraphs:
            if "地點｜" not in text and "展覽地點｜" not in text:
                continue
            loc_text = text.split("｜", 1)[1].strip()
            # Case 3: 展區名（屏菸...）
            if "（屏菸" in loc_text:
                return loc_text.split("（", 1)[0].strip()
            # 移除尾端地址括號
            loc_text = re.sub(r"\s*[(（][^)）]*[)）]", "", loc_text).strip()
            # Case 2: 屏菸1936文化基地 · 展區名
            if " · " in loc_text:
                return loc_text.split(" · ", 1)[1].strip()
            # Case 1: 屏菸1936文化基地展區名
            result = re.sub(r"屏菸\s*1936\s*文化基地", "", loc_text).strip()
            return result if result else None

        return None

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.css_first("meta[property='og:image']").attributes.get("content")

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.css_first("meta[property='og:url']").attributes.get("content")
