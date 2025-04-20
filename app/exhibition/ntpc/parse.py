import re

import bs4

from helpers.parse_helper import ParseInit


class NTPCParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("a").get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        pass

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img").get("src")

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.ceramics.ntpc.gov.tw" + self.item.find("a").get("href")


def normalize_date_range(text: str) -> str | None:
    pattern1 = re.match(r"(\d{4})\.(\d{1,2})/(\d{1,2}).*?~(\d{1,2})/(\d{1,2})", text)
    if pattern1:
        year, m1, d1, m2, d2 = pattern1.groups()
        start_date = f"{year}-{int(m1):02d}-{int(d1):02d}"
        end_date = f"{year}-{int(m2):02d}-{int(d2):02d}"
        return f"{start_date} ~ {end_date}"

    pattern2 = re.match(
        r"(\d{4})年(\d{1,2})月(\d{1,2})日[~至\-]+(\d{1,2})月(\d{1,2})日", text
    )
    if pattern2:
        year, m1, d1, m2, d2 = pattern2.groups()
        start_date = f"{year}-{int(m1):02d}-{int(d1):02d}"
        end_date = f"{year}-{int(m2):02d}-{int(d2):02d}"
        return f"{start_date} ~ {end_date}"

    return None
