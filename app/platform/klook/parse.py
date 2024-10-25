import datetime as dt
import re

from helpers.parse_helper import ParseInit
from helpers.utils_helper import this_date_year


def chinese_date_format(raw_date_string: str) -> str:
    if "年" in raw_date_string:
        pattern = r"(\d{4})年(\d{1,2})月(\d{1,2})日"
        match = re.search(pattern, raw_date_string)
        if match:
            year = match.group(1)
            month = match.group(2)
            day = match.group(3)
            return f"{year}-{int(month):02d}-{int(day):02d}"
        else:
            return "-"
    else:
        year = dt.datetime.now().year
        pattern = r"(\d{1,2})月(\d{1,2})日"
        match = re.search(pattern, raw_date_string)
        if match:
            month = match.group(1)
            day = match.group(2)
            return f"{year}-{int(month):02d}-{int(day):02d}"
        else:
            return "-"


class KLookParse(ParseInit):
    def __init__(self, item: dict | dict):
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
                runtime_title = (
                    titles[0] if titles[1] in {"展覽"} else " - ".join(titles)
                )

        elif len(titles) == 3:
            runtime_address = titles[-1]
            runtime_title = (
                titles[0] if titles[1] in {"展覽"} else " - ".join(titles[:2])
            )
        elif len(titles) == 5:
            runtime_title = titles[3]
            runtime_address = titles[2]
        else:
            runtime_title = text.strip()

        return runtime_title, runtime_address

    def get_title(self, *args, **kwargs) -> str:
        raw_title = self.item.get("title")
        runtime_title, _ = self.title_address_filter(raw_title)
        return runtime_title

    def date_format(self, raw_date_string: str) -> str:
        this_year = this_date_year()
        if "日" in raw_date_string:
            if "年" in raw_date_string:
                re_date_string = raw_date_string
            else:
                re_date_string = f"{this_year}年{raw_date_string}"
            use_format = "%Y年%m月%d日"
        else:
            if "," in raw_date_string:
                re_date_string = raw_date_string
            else:
                re_date_string = f"{raw_date_string}, {this_year}"
            use_format = "%b %d, %Y"
        return dt.datetime.strptime(re_date_string, use_format).strftime("%Y-%m-%d")

    def get_date(self, *args, **kwargs) -> str:
        date_list = self.item.get("date_list", None)
        if date_list is None:
            return ""
        raw_date_string = date_list[0].get("date")

        split_result = raw_date_string.split("-")
        if len(split_result) == 1:
            one_date = split_result[0].replace("(週日)", "").strip()
            return self.date_format(one_date)
        else:
            start_string, end_string = raw_date_string.split("-")
            start_string = (
                start_string.strip().split("(")[0].replace("(週日)", "").strip()
            )
            end_string = end_string.strip().split("(")[0].replace("(週日)", "").strip()
            return f"{self.date_format(start_string)} ~ {self.date_format(end_string)}"

    def get_address(self, *args, **kwargs) -> str:
        raw_title = self.item.get("title")
        _, runtime_address = self.title_address_filter(raw_title)
        return runtime_address

    def get_figure(self, *args, **kwargs) -> str:
        figure = self.item.get("image_url")
        return figure

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.get("event_url")
