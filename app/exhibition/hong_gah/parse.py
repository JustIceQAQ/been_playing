import datetime
import urllib.parse

import bs4

from helpers.parse_helper import ParseInit


def format_date_ranges(raw_text: str) -> str | None:
    result = None
    for line in raw_text.strip().splitlines():
        if not line.strip():
            continue
        start_str, end_str = line.split("-")

        if len(end_str) == 5:
            start_year = start_str.split(".")[0]
            end_str = f"{start_year}.{end_str}"
        elif len(end_str) == 10 and end_str.count(".") == 2:
            pass
        else:
            start_year = start_str.split(".")[0]
            if "." in end_str:
                end_str = f"{start_year}.{end_str}"
            else:
                raise ValueError(f"無法解析的日期格式: {line}")
        start_date = datetime.datetime.strptime(start_str, "%Y.%m.%d").strftime(
            "%Y-%m-%d"
        )
        end_date = datetime.datetime.strptime(end_str, "%Y.%m.%d").strftime("%Y-%m-%d")
        result = f"{start_date} ~ {end_date}"
    return result


class HongGahParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
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
