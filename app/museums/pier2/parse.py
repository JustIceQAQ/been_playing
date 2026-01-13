import bs4

from helpers.parse_helper import ParseInit


class Pier2Parse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("thetitle").strip()

    def get_date(self, *args, **kwargs) -> str | None:
        return (
            self.item.get("starttime").strip()
            + " ~ "
            + self.item.get("endtime").strip()
        )

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.get("place").strip()

    def get_figure(self, *args, **kwargs) -> str | None:
        if (the_photo := self.item.get("thephoto", None)) is not None:
            return "https://pier2.org/" + the_photo

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://pier2.org/exhibition/info/{info_code}/".format(
            info_code=self.item.get("id")
        )
