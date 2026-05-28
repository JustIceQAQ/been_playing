import datetime
import urllib.parse

import bs4

from helpers.parse_helper import ParseInit


def format_date_ranges(raw_text: str) -> str | None:
    if not raw_text:
        return None

    def normalize_part(s: str) -> str:
        """將每個 . 分隔的數字部分去除多餘前導零，例如 '013' -> '13'"""
        parts = s.split(".")
        normalized = []
        for i, p in enumerate(parts):
            if i == 0:
                normalized.append(p)  # 年份保持原樣
            else:
                try:
                    normalized.append(str(int(p)))  # 去除前導零
                except ValueError:
                    normalized.append(p)
        return ".".join(normalized)

    def parse_date(date_str: str) -> str:
        date_str = normalize_part(date_str.strip())
        return datetime.datetime.strptime(date_str, "%Y.%m.%d").strftime("%Y-%m-%d")

    line = raw_text.strip()

    if "-" not in line:
        # 單一日期，例如 '2026.06.13'
        try:
            return parse_date(line)
        except ValueError:
            raise ValueError(f"無法解析的日期格式: {line}")

    # 有 '-'，嘗試切割為 start / end
    parts = line.split("-")

    if len(parts) == 2:
        start_str, end_str = parts[0].strip(), parts[1].strip()
    else:
        raise ValueError(f"無法解析的日期格式: {line}")

    # 補全 end_str 的年份
    if len(end_str) <= 5 and end_str.count(".") == 1:
        # 例如 end_str = '08.23'，補上 start 的年份
        start_year = start_str.split(".")[0]
        end_str = f"{start_year}.{end_str}"
    elif len(end_str) == 10 and end_str.count(".") == 2:
        pass  # 已是完整日期，例如 '2026.08.23'
    else:
        start_year = start_str.split(".")[0]
        if "." in end_str:
            end_str = f"{start_year}.{end_str}"
        else:
            raise ValueError(f"無法解析的日期格式: {line}")

    start_date = parse_date(start_str)
    end_date = parse_date(end_str)

    return f"{start_date} ~ {end_date}"


class HongGahParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        img_element = self.item.find("img")
        return img_element.attrs["alt"]

    def get_date(self, *args, **kwargs) -> str | None:
        heading = self.item.find("div", {"class": "heading"})
        raw_date = heading.next_element.next_element.next_element.next_element.get_text().strip()
        date_range = format_date_ranges(raw_date)
        return date_range

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        img_element = self.item.find("img")
        return urllib.parse.quote(img_element.attrs["src"], safe=":/")

    def get_source_url(self, *args, **kwargs) -> str | None:
        source_url = self.item.find("a", {"class": "card-image"})["href"]
        return source_url
