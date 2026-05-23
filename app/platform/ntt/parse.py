from helpers.parse_helper import ParseInit


class NTTParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        name = self.item.get("name")
        if name is None:
            return None
        return name

    def get_date(self, *args, **kwargs) -> str | None:
        subject = self.item.get("subject")
        if subject is None:
            return None
        return subject.replace("～", " ~ ")

    def get_address(self, *args, **kwargs) -> str | None:
        address = self.item.get("address")
        if address is None:
            return None
        return address

    def get_figure(self, *args, **kwargs) -> str | None:
        thumb = self.item.get("thumb")
        if thumb is None:
            return None
        return thumb

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        url = self.item.get("url")
        if url is None:
            return None
        return url
