import bs4

from helpers.parse_helper import ParseInit

import re


def format_exhibition_date(date_str):
    clean_str = date_str.strip()
    pattern = r"(\d{4})年(\d{1,2})月(\d{1,2})日[至至~](\d{4})?年?(\d{1,2})月(\d{1,2})日"
    match = re.search(pattern, clean_str)

    if match:
        groups = match.groups()
        year1, month1, day1 = groups[0], groups[1], groups[2]
        year2 = groups[3] if groups[3] else year1
        month2, day2 = groups[4], groups[5]
        formatted_date = (
            f"{int(year1):04d}-{int(month1):02d}-{int(day1):02d} "
            f"~ {int(year2):04d}-{int(month2):02d}-{int(day2):02d}"
        )
        return formatted_date
    return None


class NtcCeramicsParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("a").get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        raw_date = self.item.find("div", {"class": "desc"}).get_text(strip=True)
        return format_exhibition_date(raw_date)

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.ceramics.ntpc.gov.tw" + self.item.find("a").get("href")
