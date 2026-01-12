import bs4

from helpers.parse_helper import ParseInit


class TnamMuseumParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("title").strip()

    def get_date(self, *args, **kwargs) -> str | None:
        dates = self.item.find_all("span", class_="date")
        if len(dates) == 0:
            return None
        if len(dates) == 1:
            return dates[0].get_text(strip=True).replace("/", "-")

        start_date, end_date = dates
        ok_start_date = start_date.get_text(strip=True).replace("/", "-")
        ok_end_date = end_date.get_text(strip=True).replace("/", "-")

        return f"{ok_start_date} ~ {ok_end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "location"}).get_text(strip=True)

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://www.tnam.museum/" + self.item.find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.tnam.museum/" + self.item.get("href").strip()
