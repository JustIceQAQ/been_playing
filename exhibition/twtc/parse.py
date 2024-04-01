import datetime

import bs4

from helper.parse_helper import ParseInit


class TWTCParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item
        self.item_tds = item.select("td")

    def get_title(self, *args, **kwargs) -> str:
        return self.item_tds[1].get_text()

    def get_date(self, *args, **kwargs) -> str:
        this_year = datetime.datetime.now().year
        raw_date_string = self.item_tds[0].get_text()
        start_date_str, end_date_str = raw_date_string.split("~")
        start_date_month, start_date_day = start_date_str.split("/")
        end_date_month, end_date_day = end_date_str.split("/")
        string_date = f"{this_year}-{start_date_month}-{start_date_day}"
        end_date_year = (this_year + 1) if int(end_date_month) < int(start_date_month) else this_year
        end_date = f"{end_date_year}-{int(end_date_month)}-{end_date_day}"
        return f"{string_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str:
        return self.item_tds[4].get_text()

    def get_figure(self, *args, **kwargs) -> str:
        return ""

    def get_source_url(self, *args, **kwargs) -> str:
        nth_child_a = self.item_tds[1].select("a")
        if len(nth_child_a) > 1:
            return nth_child_a[0].get("href", None)
        else:
            return "https://twtc.com.tw/" + nth_child_a[0].get("href", None)
