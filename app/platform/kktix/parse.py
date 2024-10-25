import datetime

from helpers.parse_helper import ParseInit


class KKTixParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.get("name")

    def get_date(self, *args, **kwargs) -> str:
        start_at: int | None = self.item.get("start_at", None)
        if start_at is None:
            return ""
        start_at_datetime = datetime.datetime.fromtimestamp(start_at)
        return start_at_datetime.strftime("%Y-%m-%d")

    def get_address(self, *args, **kwargs) -> str:
        return ""

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.get("og_image_url")

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.get("public_url")
