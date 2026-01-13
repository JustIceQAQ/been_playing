import bs4

from helpers.parse_helper import ParseInit
from helpers.utils_helper import roc_era_to_ad


def roc_era_date_to_ad_date(this_date: str) -> str:
    this_date = this_date.strip()
    roc_era_year, month, day = this_date.split("-")
    year = roc_era_to_ad(int(roc_era_year))
    return f"{year}-{month}-{day}"


class TaipeiExPoParkParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("a").get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        date_range = self.item.find("i", {"class": "mark"}).get_text().strip()
        date_string = ""
        if "~" in date_range:
            start_date, end_date = date_range.split("~")
            start_date_ok = roc_era_date_to_ad_date(start_date)
            end_date_ok = roc_era_date_to_ad_date(end_date)
            date_string = " ~ ".join([start_date_ok, end_date_ok])
        else:
            date_string = roc_era_date_to_ad_date(date_range)
        return date_string

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.find("i", {"class": "info_list_location"}).get_text()

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img").get("src")

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.expopark.taipei/" + self.item.find("a").get("href")
