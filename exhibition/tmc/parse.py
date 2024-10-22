import re

import bs4

from helper.parse_helper import ParseInit


class TMCParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.get("title")

    def get_date(self, *args, **kwargs) -> str:
        raw_date_string = self.item.find("span", {"class": "date"}).get_text().strip()

        raw_date_string = raw_date_string.replace("-", "~")

        subbed_string = re.sub(r"(\(.\))", "", raw_date_string)

        return subbed_string.replace(".", "-")

    def get_address(self, *args, **kwargs) -> str:
        return self.safe_get_text(
            self.item.find("span", {"class": "location"}).get_text()
        )

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.find("img").get("src")

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.get("href")
