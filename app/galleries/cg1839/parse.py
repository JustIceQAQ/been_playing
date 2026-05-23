import re

import bs4

from helpers.parse_helper import ParseInit


class CG1839Parse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h1", {"class": "entry-title"}).get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        elements = self.item.select("strong")
        date_text = ""
        for el in elements:
            if "展期" in el.get_text():
                date_text = el.get_text(separator=" ", strip=True)
                break
        match = re.search(r"(\d{4})年(\d{2})月(\d{2})日?[–~](\d{2})月(\d{2})", date_text)
        if match:
            year = match.group(1)
            start_month = match.group(2)
            start_day = match.group(3)
            end_month = match.group(4)
            end_day = match.group(5)

            start_date = f"{year}-{start_month}-{start_day}"
            end_date = f"{year}-{end_month}-{end_day}"
            result = f"{start_date} ~ {end_date}"
            return result

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("figure", {"class": "wp-block-image"}).find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.find("link", {"rel": "canonical"}).get("href")
