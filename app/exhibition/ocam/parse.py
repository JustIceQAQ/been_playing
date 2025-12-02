import bs4

from helpers.parse_helper import ParseInit


class OCAMParse(ParseInit):
    def __init__(self, item: bs4.BeautifulSoup):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("a").get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        parent_div = self.item.find("div", class_="activityicon icon-acttime")

        all_sub_divs = parent_div.find_all("div")

        date_div = all_sub_divs[1]
        date_strings = list(date_div.stripped_strings)
        if len(date_strings) >= 3:
            start_date = date_strings[0]
            end_date = date_strings[2]
            return start_date + " ~ " + end_date

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://www.ymculture.org.tw" + self.item.find(
            "img", {"class": "block"}
        ).get("src")

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.ymculture.org.tw" + self.item.find(
            "a",
        ).get("href")
