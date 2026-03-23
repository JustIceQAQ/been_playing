from helpers.parse_helper import ParseInit


class Pier2Parse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        the_title = self.item.get("thetitle")
        if the_title:
            return the_title.strip()

    def get_date(self, *args, **kwargs) -> str | None:
        start_time = self.item.get("starttime")
        end_time = self.item.get("endtime")
        if start_time and end_time:
            return start_time.strip() + " ~ " + end_time.strip()

    def get_address(self, *args, **kwargs) -> str | None:
        place = self.item.get("place")
        if place:
            return place.strip()

    def get_figure(self, *args, **kwargs) -> str | None:
        the_photo = self.item.get("thephoto")
        if the_photo is not None:
            return "https://pier2.org/" + the_photo

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        info_code = self.item.get("id")
        if info_code:
            return "https://pier2.org/exhibition/info/{info_code}/".format(info_code=info_code)
