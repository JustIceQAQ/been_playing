import bs4

from helper.parse_helper import ParseInit


class NTCArtMuseumMainParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("img").get("alt")

    def get_date(self, *args, **kwargs) -> str:
        date_format = ""
        year = self.item.select_one("div.text-group > div.upper-text > h1").get_text().strip()
        dates = self.item.select_one("div.text-group > div.bottom-text").get_text().strip()
        left_date, _, right_date = dates.partition("—")
        clean_left_date = left_date.strip()
        clean_right_date = right_date.strip()
        if clean_left_date:
            left_month, _, left_month_day = clean_left_date.partition(".")
            date_format += f"{year}-{left_month}-{left_month_day}"
        if clean_right_date:
            right_month, _, right_month_day = clean_right_date.partition(".")
            if int(right_month) < int(right_month):
                year = int(year) + 1
            date_format += f" ~ {year}-{right_month}-{right_month_day}"
        return date_format

    def get_address(self, *args, **kwargs) -> str:
        return ""

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.find("img").get("src")

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.get("href")
        )


class NTCArtMuseumOtherParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("h2", {"class": "bigTitle"}).get_text().strip()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.find("p", {"class": "bigDate"}).get_text().strip().replace("—", "~")

    def get_address(self, *args, **kwargs) -> str:
        return ""

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.find("img").get("src")

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.get("href")
        )
