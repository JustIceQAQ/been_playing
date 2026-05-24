import re

from helpers.parse_helper import ParseInit
import datetime
from helpers.utils_helper import get_date as get_the_date


from selectolax.lexbor import LexborNode


class HuaLien1913Parse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        title = self.item.css_first("div.title a").text(strip=True)
        if not title:
            return None

        # 移除日期區段，格式如：
        # 5/22-5/24、12/13-5/10、1/25、1/28、1/17
        # 連同前後的空白、【】外的空格一起清除
        title = re.sub(r"\d{1,2}/\d{1,2}(?:[、\-]\d{1,2}/\d{1,2})*", "", title)

        # 清理殘留的多餘空白與開頭結尾空白
        title = re.sub(r"\s+", " ", title).strip()

        return title or None

    def get_date(self, *args, **kwargs) -> str | None:
        title = self.item.css_first("div.title a").text(strip=True)
        if not title:
            return None

        # 抓出日期部分，支援格式如 5/22-5/24、1/25、1/28、12/13-5/10
        pattern = r"(\d{1,2}/\d{1,2})"
        matches = re.findall(pattern, title)

        if not matches:
            return None

        base_year = get_the_date.now_year  # 資料基準年

        def parse_md(s):
            """將 'M/D' 拆成 (month, day)"""
            m, d = s.split("/")
            return int(m), int(d)

        def resolve_year(month, ref_year, ref_month=None, is_end=False):
            """
            決定年份：
            - 若是結束日期且月份 < 開始月份，視為跨年（+1 → 不對，需反過來）
            實際上：資料基準是 2026，若開始月份 > 結束月份，
            代表開始在前一年。
            """
            return ref_year

        if len(matches) == 1:
            # 單日
            m, d = parse_md(matches[0])
            return datetime.date(base_year, m, d).strftime("%Y-%m-%d")

        else:
            # 區間（取第一個為 start，最後一個為 end）
            start_str = matches[0]
            end_str = matches[-1]

            sm, sd = parse_md(start_str)
            em, ed = parse_md(end_str)

            # 跨年判斷：結束月份 < 開始月份
            # 代表 start 在前一年，end 在 base_year
            if em < sm:
                start_year = base_year - 1
                end_year = base_year
            else:
                start_year = base_year
                end_year = base_year

            start_date = datetime.date(start_year, sm, sd).strftime("%Y-%m-%d")
            end_date = datetime.date(end_year, em, ed).strftime("%Y-%m-%d")

            return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.css_first("img").attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.css_first("div.title a").attributes.get("href")
