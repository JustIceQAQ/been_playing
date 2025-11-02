from helpers.parse_helper import ParseInit


class GaCcParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("name")

    def get_date(self, *args, **kwargs) -> str | None:
        event_begin_at = self.item.get("eventBeginAt", None)
        event_end_at = self.item.get("eventEndAt", None)
        if event_begin_at is None:
            return None
        if event_end_at is None:
            return event_begin_at

        return f"{event_begin_at} ~ {event_end_at}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.get("image")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        return [self.item.get("eventCategoryName")]

    def get_source_url(self, *args, **kwargs) -> str | None:
        url_id = self.item.get("id")
        return f"https://www.gacc.org.tw/TW/events/{url_id}"
