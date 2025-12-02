import bs4

from helpers.parse_helper import ParseInit


class AAAArchivesParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("a").get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        i_calendar = self.item.find("i", class_="i_calendar")
        if i_calendar:
            raw_date = i_calendar.next_sibling
            if raw_date:
                return raw_date.strip().replace("/", "-")

    def get_address(self, *args, **kwargs) -> str | None:
        i_location = self.item.find("i", class_="i_location")
        if i_location:
            raw_location = i_location.next_sibling
            if raw_location:
                return raw_location.strip()

    def get_figure(self, *args, **kwargs) -> str | None:
        img = self.item.find("img")
        if img:
            src = img.get("src")
            return "https://aaa.archives.tw" + src

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        i_man = self.item.find("i", class_="i_man")
        if i_man:
            raw_man = i_man.next_sibling
            if raw_man:
                return raw_man.split(",")

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.find("a").get("href")
