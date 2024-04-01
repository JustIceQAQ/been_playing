import datetime
import re

import bs4
import cssutils

from helper.parse_helper import ParseInit


def chinese_date_format(raw_date_string: str) -> str:
    if "年" in raw_date_string:
        pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
        match = re.search(pattern, raw_date_string)
        if match:
            year = match.group(1)
            month = match.group(2)
            day = match.group(3)
            return f"{year}-{month}-{day}"
        else:
            return ""
    else:
        year = datetime.datetime.now().year
        pattern = r'(\d{1,2})月(\d{1,2})日'
        match = re.search(pattern, raw_date_string)
        if match:
            month = match.group(1)
            day = match.group(2)
            return f"{year}-{month}-{day}"
        else:
            return ""


class KLookParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def title_address_filter(self, text: str) -> (str, str):
        runtime_address = "-"
        titles = text.strip().split("｜")

        if len(titles) == 1:
            runtime_title = titles[-1]

        elif len(titles) == 2:
            if ("預售" in titles[0]) and ("優惠" in titles[0]) and ("折" in titles[0]):
                runtime_title = titles[1]
            else:
                runtime_title = titles[0] if titles[1] in {"展覽"} else " - ".join(titles)

        elif len(titles) == 3:
            runtime_address = titles[-1]
            runtime_title = titles[0] if titles[1] in {"展覽"} else " - ".join(titles[:2])
        elif len(titles) == 5:
            runtime_title = titles[3]
            runtime_address = titles[2]
        else:
            runtime_title = text.strip()

        return runtime_title, runtime_address

    def get_title(self, *args, **kwargs) -> str:
        raw_title = self.item.select_one("h3.title").get_text()
        runtime_title, _ = self.title_address_filter(raw_title)
        return runtime_title

    def get_date(self, *args, **kwargs) -> str:
        raw_date_string = self.item.select_one("div.dates > * > span").get_text()
        subbed_string = re.sub(r'(\(..\))', '', raw_date_string)
        raw_date_string_strip = subbed_string.strip("-")

        if len(raw_date_string_strip) == 1:
            start_date = raw_date_string_strip[0].strip()
            return chinese_date_format(start_date)
        else:
            start_date, end_date = raw_date_string_strip
            return f"{chinese_date_format(start_date)}~{chinese_date_format(end_date)}"

    def get_address(self, *args, **kwargs) -> str:
        raw_title = self.item.select_one("h3.title").get_text()
        _, runtime_address = self.title_address_filter(raw_title)
        return runtime_address

    def get_figure(self, *args, **kwargs) -> str:
        dev_style = self.item.select_one("div.left > * > .img").get("style")
        style = cssutils.parseStyle(dev_style)

        return (
            url.replace("url(", "")[:-1].replace('"', "")
            if (url := style["background-image"])
            else "-"
        )

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.get("href")
