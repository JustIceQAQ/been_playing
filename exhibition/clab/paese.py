import urllib.parse

from bs4 import Tag

from helper.parse_helper import ParseInit


def clean_date(value: Tag) -> str:
    year = (
        value.find("p", {"class": "a-dateTime__year"})
        .get_text()
        .strip()
        .split(".")[0]
        .strip()
    )
    month_day = (
        value.find("p", {"class": "a-dateTime__text"})
        .get_text()
        .strip()
        .split("(")[0]
        .split(".")
    )
    month, day = month_day
    return f"{year}-{month}-{day}"


class CLabParse(ParseInit):
    def __init__(self, item: Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("p", {"class": "a-base-card__title"}).get_text().strip()

    def get_date(self, *args, **kwargs) -> str:
        date_raw = self.item.find("div", {"class": "a-dateTime__wrapper"})
        dates = date_raw.find_all("div")
        result_date = "-"
        if len(dates) == 2:
            start_date, end_date = dates
            result_date = f"{clean_date(start_date)} ~ {clean_date(end_date)}"
        elif len(dates) == 1:
            once_day = dates[0]
            result_date = f"{clean_date(once_day)}"
        else:
            pass
        return result_date

    def get_address(self, *args, **kwargs) -> str:
        return (
            self.item.find("p", {"class": "a-base-card__location"}).get_text().strip()
        )

    def get_figure(self, *args, **kwargs) -> str:
        div = self.item.find("div", {"class": "a-base-card__thumbnail"})
        if div is None:
            return "-"
        dev_style = div.attrs.get(":style")
        pc_image = dev_style.split(":")[-1]

        return f"https:{urllib.parse.quote(pc_image[:-3])}"

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.find("a", {"class": "a-base-card__media"})["href"]
