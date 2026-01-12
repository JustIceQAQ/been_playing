import datetime
import re

import bs4

from helpers.parse_helper import ParseInit


class MoCaTaipeiParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("h3", {"class": "imgTitle"}).get_text()

    def get_date(self, *args, **kwargs) -> str:
        raw_string = self.item.find("div", {"class": "dateBox"}).get_text()
        regulated = re.findall(
            r"(?P<year>\d{4})\s*(?P<month>\d{2})\s\/\s(?P<day>\d{2})", raw_string
        )
        start_date_regulated, end_date_regulated = regulated
        start_date = datetime.date(
            int(start_date_regulated[0]),
            int(start_date_regulated[1]),
            int(start_date_regulated[2]),
        ).isoformat()
        end_date = datetime.date(
            int(end_date_regulated[0]),
            int(end_date_regulated[1]),
            int(end_date_regulated[2]),
        ).isoformat()

        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        sub_title = self.item.find("h4", {"class": "imgSubTitle"}).get_text(strip=True)
        if not sub_title:
            return None
        if "MoCA Video" in sub_title:
            return f"台北當代藝術館廣場電視牆 ({sub_title})"
        return sub_title

    def get_figure(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.select_one("figure.imgFrame img")["data-src"]
        )

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("a.textFrame")["href"]
