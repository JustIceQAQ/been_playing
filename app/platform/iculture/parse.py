from helpers.parse_helper import ParseInit


class ICultureParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        raw_start_date: str | None = self.item.get("startDate", None)
        if raw_start_date is None:
            return None

        start_date: str = raw_start_date.split("T")[0]

        raw_end_date: str | None = self.item.get("endDate", None)
        if raw_end_date is None:
            return start_date

        end_date: str = raw_end_date.split("T")[0]

        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.get("eventLocationName")

    def get_figure(self, *args, **kwargs) -> str | None:
        image_url = self.item.get("imageUrl")
        if image_url is None:
            return None
        return "https://cloud.culture.tw" + self.item.get("imageUrl")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        tags = []
        for i in range(1, 4):
            ev_char = self.item.get(f"evChar{i}", None)
            if ev_char is None:
                continue
            tags.append(ev_char)

        if tags:
            return tags

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.get("sourceWebSiteSales")
