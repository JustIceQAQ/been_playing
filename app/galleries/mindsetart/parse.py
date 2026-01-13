import ast
import re

import bs4

from helpers.parse_helper import ParseInit


class MindSetArtParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h2").get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        text = self.item.find("span", {"class": "date"}).get_text(strip=True)
        nums = re.findall(r"\d+", text)

        if len(nums) == 6:
            start_year, start_month, start_day = nums[0:3]
            end_year, end_month, end_day = nums[3:6]
        elif len(nums) == 5:
            start_year, start_month, start_day = nums[0:3]
            end_year = start_year
            end_month, end_day = nums[3:5]
        else:
            raise ValueError("Invalid date format")

        start_date = (
            f"{int(start_year):04d}-{int(start_month):02d}-{int(start_day):02d}"
        )
        end_date = f"{int(end_year):04d}-{int(end_month):02d}-{int(end_day):02d}"

        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        data_responsive_src = self.item.find("img").get("data-responsive-src")
        srcs = ast.literal_eval(data_responsive_src)
        return srcs["750"]

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        href = self.item.find("a").get("href")

        return "https://www.art-msac.com" + href
