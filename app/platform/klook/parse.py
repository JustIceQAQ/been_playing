import datetime as dt
import re

from helpers.parse_helper import ParseInit
from helpers.utils_helper import get_this_date_year


def chinese_date_format(raw_date_string: str) -> str | None:
    if "年" in raw_date_string:
        pattern = r"(\d{4})年(\d{1,2})月(\d{1,2})日"
        match = re.search(pattern, raw_date_string)
        if match:
            year = match.group(1)
            month = match.group(2)
            day = match.group(3)
            return f"{year}-{int(month):02d}-{int(day):02d}"
        else:
            return None
    else:
        year = dt.datetime.now().year
        pattern = r"(\d{1,2})月(\d{1,2})日"
        match = re.search(pattern, raw_date_string)
        if match:
            month = match.group(1)
            day = match.group(2)
            return f"{year}-{int(month):02d}-{int(day):02d}"
        else:
            return None


def check_use_to_split(text: str, check_list: list[str]) -> str | None:
    for check in check_list:
        if check in text:
            return check
    return None


class KLookParse(ParseInit):
    def __init__(self, item: dict | dict):
        self.item = item

    def title_address_filter(self, text: str) -> tuple[str, str | None]:
        ok_text = text.strip()
        use_split = check_use_to_split(ok_text, ["|", "｜"])

        if use_split is None:
            return ok_text, None
        parts = ok_text.split(use_split)
        if len(parts) == 1:
            return parts[0].strip(), None
        address = parts[0].strip()
        title = " ".join(p.strip() for p in parts[1:])
        return title, address

    def get_title(self, *args, **kwargs) -> str | None:
        raw_title = self.item.get("title")
        if raw_title is None:
            return None
        runtime_title, _ = self.title_address_filter(raw_title)
        return runtime_title

    def replace_1_7(self, value: str) -> str:
        for i in {"(週日)", "(週一)", "(週二)", "(週三)", "(週四)", "(週五)", "(週六)"}:
            value = value.replace(i, "").strip()
        return value

    def date_format(self, raw_date_string: str) -> str:
        this_year = get_this_date_year()
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

    def get_date(self, *args, **kwargs) -> str | None:
        date_list = self.item.get("date_list", None)
        if date_list is None:
            return ""
        raw_date_string = date_list[0].get("date")

        split_result = raw_date_string.split("-")
        if len(split_result) == 1:
            one_date = self.replace_1_7(split_result[0])
            return self.date_format(one_date)
        else:
            start_string, end_string = raw_date_string.split("-")
            start_string = self.replace_1_7(start_string.strip().split("(")[0])
            end_string = self.replace_1_7(end_string.strip().split("(")[0])
            return f"{self.date_format(start_string)} ~ {self.date_format(end_string)}"

    def get_address(self, *args, **kwargs) -> str | None:
        raw_title = self.item.get("title")
        if raw_title is None:
            return None
        _, runtime_address = self.title_address_filter(raw_title)
        return runtime_address

    def get_figure(self, *args, **kwargs) -> str | None:
        figure = self.item.get("image_url")
        return figure

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        raw_tags: list[dict[str, str]] | None = self.item.get("tags")
        if raw_tags:
            return [tag.get("text") for tag in raw_tags if tag.get("text") is not None]

        return None

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.get("event_url")
