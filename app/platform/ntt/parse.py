from helpers.parse_helper import ParseInit


class NTTParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("name")

    def get_date(self, *args, **kwargs) -> str | None:
        return self.item.get("subject").replace("～", " ~ ")

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.get("address")

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.get("thumb")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.get("url")
