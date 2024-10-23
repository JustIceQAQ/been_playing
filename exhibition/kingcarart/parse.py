import datetime as dt

from bs4 import Tag

from helper.parse_helper import ParseInit
from helpers.utils_helper import date_now


def parse_date(date_string: str) -> dt.date:
    return dt.datetime.strptime(date_string, "%b. %d %Y").date()


class KingCarArtParse(ParseInit):
    def __init__(self, item: Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        select_one_result = self.item.select_one(
            "div.ex-info > h2 > span.tw"
        ) or self.item.select_one("div.ex-info > h2 > span")
        return select_one_result.get_text() if select_one_result else "-"

    def get_date(self, *args, **kwargs) -> str:
        raw_date = (
            div.get_text()
            if (div := self.item.find("div", {"class": "ex-date"}))
            else ""
        )
        if not raw_date:
            return "-"

        first_date_raw, second_date_raw = raw_date.split("→")
        first_date_raw = first_date_raw.strip()
        second_date_raw = second_date_raw.strip()

        second_date_year = date_now().year
        if len(second_date_raw.split(" ")) == 3:
            second_date = parse_date(second_date_raw)
            second_date_year = second_date.year
        else:
            return "-"

        first_date_split = first_date_raw.split(" ")
        if len(first_date_split) == 3:
            first_date = parse_date(first_date_raw)
        else:
            first_date = parse_date(f"{first_date_raw} {second_date_year}")

        return f'{first_date.strftime("%Y-%m-%d")} ~ {second_date.strftime("%Y-%m-%d")}'

    def get_address(self, *args, **kwargs) -> str:
        return ", ".join(
            span.get_text().strip() if span else ""
            for span in self.item.select("div.ex-location > span")
        )

    def get_figure(self, *args, **kwargs) -> str:
        div = self.item.find("div", {"class": "ex-img"})
        if div is None:
            return "-"
        dev_style = div.attrs.get("style")
        image = dev_style.split(":")[-1]
        return f"https:{image[:-2]}"

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.find("a")["href"]
