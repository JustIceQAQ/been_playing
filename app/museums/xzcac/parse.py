import datetime
import re

from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit
from helpers.utils_helper import get_date as get_the_date


class XZCACParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        title = self.item.css_first("meta[name='Title']").attributes.get("content")
        if not title:
            return None

        title = title.strip()
        title = re.sub(r"\d{1,2}/\d{1,2}(?:[、\-]\d{1,2}/\d{1,2})*", "", title)
        title = re.sub(r"\s+", " ", title).strip()
        return title or None

    def get_date(self, *args, **kwargs) -> str | None:
        title = self.item.css_first("meta[name='Title']").attributes.get("content")
        if not title:
            return None
        title = title.strip()

        # 同時比對「Y/M/D」(民國年，通常 3 碼) 與「M/D」兩種格式
        # 順序很重要：先比對三段式，避免被兩段式規則搶先誤判
        pattern = r"(\d{1,3}/\d{1,2}/\d{1,2}|\d{1,2}/\d{1,2})"
        matches = re.findall(pattern, title)

        if not matches:
            return None

        base_year = get_the_date.now_year  # 資料基準年（西元）

        def parse_token(token: str):
            """
            將擷取到的字串解析為 (year_or_None, month, day)。
            若是三段式，年份視為民國年，轉換成西元年（民國年 + 1911）。
            """
            parts = token.split("/")
            if len(parts) == 3:
                roc_year, m, d = parts
                year = int(roc_year) + 1911
                return year, int(m), int(d)
            else:
                m, d = parts
                return None, int(m), int(d)

        if len(matches) == 1:
            year, m, d = parse_token(matches[0])
            year = year or base_year
            return datetime.date(year, m, d).strftime("%Y-%m-%d")

        start_year, sm, sd = parse_token(matches[0])
        end_year, em, ed = parse_token(matches[-1])

        if start_year is None and end_year is None:
            # 都沒有明確年份，沿用原本「結束月 < 開始月 -> 跨年」的假設
            if em < sm:
                start_year, end_year = base_year - 1, base_year
            else:
                start_year = end_year = base_year
        elif start_year is None:
            # 只有結束日期帶年份（例如你截圖那筆資料的情況）
            start_year = end_year - 1 if em < sm else end_year
        elif end_year is None:
            # 只有開始日期帶年份
            end_year = start_year + 1 if em < sm else start_year
        # 若兩者皆有明確年份，則直接使用，不做額外推算

        start_date = datetime.date(start_year, sm, sd).strftime("%Y-%m-%d")
        end_date = datetime.date(end_year, em, ed).strftime("%Y-%m-%d")

        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        target_img = self.item.css_first("div.img_bg img") or self.item.css_first("div.district img")
        if target_img is None:
            return None
        return target_img.attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.css_first("meta[property='og:Url']").attributes.get("content")
