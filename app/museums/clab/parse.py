from bs4 import Tag

from helpers.parse_helper import ParseInit


def clean_date(value: Tag) -> str:
    year = value.find("p", {"class": "a-dateTime__year"}).get_text().strip().split(".")[0].strip()
    month_day = value.find("p", {"class": "a-dateTime__text"}).get_text().strip().split("(")[0].split(".")
    month, day = month_day
    return f"{year}-{month}-{day}"


class CLabParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        single_event = self.item.get("singleEvent")
        if single_event is None:
            return None
        raw_date = single_event.get("date")
        if raw_date is None:
            return None
        start = raw_date.get("start").split("T")[0]
        end = raw_date.get("end").split("T")[0]
        if start == end:
            return start
        return f"{start} ~ {end}"

    def get_address(self, *args, **kwargs) -> str | None:
        single_event = self.item.get("singleEvent")
        if single_event is None:
            return None
        return single_event.get("location")

    def get_figure(self, *args, **kwargs) -> str | None:
        featured_image = self.item.get("featuredImage")
        if featured_image is None:
            return None
        return featured_image.get("node").get("sourceUrl")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        tags = self.item.get("tags")
        if tags is None:
            return None
        node = tags.get("node")
        if node is None:
            return None
        return [tag.get("name") for tag in node]

    def get_source_url(self, *args, **kwargs) -> str | None:
        slug = self.item.get("slug")
        return f"https://clab.org.tw/zh/events/{slug}"
