import re
import datetime
import bs4
import ast
from helpers.parse_helper import ParseInit


def convert_date_range(date_str):
    year_match = re.search(r"(\d{4})$", date_str.strip())
    if not year_match:
        return "找不到年份"
    year = year_match.group(1)
    clean_str = re.sub(r",?\s*\d{4}$", "", date_str.strip())
    parts = [p.strip() for p in clean_str.split("-")]
    results = []
    for part in parts:
        try:
            full_date_str = f"{part} {year}"
            dt = datetime.datetime.strptime(full_date_str, "%B %d %Y")
            results.append(dt.strftime("%Y-%m-%d"))
        except ValueError:
            try:
                dt = datetime.datetime.strptime(full_date_str, "%b %d %Y")
                results.append(dt.strftime("%Y-%m-%d"))
            except Exception:  # noqa
                raise ValueError(f"Invalid date string: {date_str}")

    return results


class RuoMuParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h2").get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        date = self.item.find("span", {"class": "date"}).get_text(strip=True)
        return " ~ ".join(convert_date_range(date))

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        data_responsive_src = self.item.find("img").get("data-responsive-src")
        srcs = ast.literal_eval(data_responsive_src)
        return srcs["750"]

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.ruomugallery.com" + self.item.find("a").get("href")
