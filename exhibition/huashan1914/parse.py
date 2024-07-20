import datetime
import re

import bs4
import cssutils

from helper.parse_helper import ParseInit


class HuaShan1914Parse(ParseInit):
    def __init__(self, item: bs4.element.Tag) -> None:
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one(
            "li > a > div > div > div.card-text > div.card-text-name"
        ).get_text()

    def get_date(self, *args, **kwargs) -> str:
        raw_string = self.item.select_one(
            "li > a > div > div > div.card-text > div.event-date"
        ).get_text()
        if "-" in raw_string:
            row_start_date, row_end_date = raw_string.split(" - ")
            regulated_start_date = re.search(
                r"((?P<year>\d{4})\.(?P<month>\d{2})\.(?P<day>\d{2}))", row_start_date
            )
            start_date = datetime.date(
                int(regulated_start_date.group("year")),
                int(regulated_start_date.group("month")),
                int(regulated_start_date.group("day")),
            )
            regulated_end_date = re.search(
                r"((?P<year>\d{4})?\.?(?P<month>\d{2})\.(?P<day>\d{2}))", row_end_date
            )
            end_date = datetime.date(
                int(
                    year
                    if (year := regulated_end_date.group("year"))
                    else start_date.year
                ),
                int(regulated_end_date.group("month")),
                int(regulated_end_date.group("day")),
            )

            cooked_string = f"{start_date.isoformat()} ~ {end_date.isoformat()}"
        else:
            # one day case
            regulated = re.search(
                r"((?P<year>\d{4})\.(?P<month>\d{2})\.(?P<day>\d{2}))", raw_string
            )
            start_date = datetime.date(
                int(regulated.group("year")),
                int(regulated.group("month")),
                int(regulated.group("day")),
            ).isoformat()
            end_date = start_date
            cooked_string = f"{start_date} ~ {end_date}"
        return cooked_string

    def get_address(self, *args, **kwargs) -> str:
        return "-"

    def get_figure(self, *args, **kwargs) -> str:
        if self.item is None:
            return "-"
        dev_style = self.item.select_one("li > a > div > div > div.card-img.wide")
        if dev_style is None:
            return "-"
        dev_style = dev_style["style"]
        style = cssutils.parseStyle(dev_style)

        return (
            url.replace("url(", "")[:-1].replace('"', "")
            if (url := style["background-image"])
            else "-"
        )

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(target_domain, self.item.select_one("li > a")["href"])
