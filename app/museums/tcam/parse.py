from helpers.parse_helper import ParseInit


class TcamParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        open_date = self.item.get("open_date")
        end_date = self.item.get("end_date")
        if open_date is None:
            return None

        if end_date is None:
            return open_date

        return f"{open_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        location = self.item.get("location")
        if location is None:
            return None
        return location.split("｜")[1].strip()

    def get_figure(self, *args, **kwargs) -> str | None:
        image = self.item.get("image")
        if image is None:
            return None
        medium_sizes = image.get("sizes", {}).get("medium", None)
        if medium_sizes is not None:
            return medium_sizes

        return image.get("url")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        category = self.item.get("category")
        if category is None:
            return None
        tags = [c.get("name") for c in category]
        return tags

    def get_source_url(self, *args, **kwargs) -> str | None:
        url = self.item.get("url")
        if url is None:
            return None
        return "https://www.tcam.museum/zh/exhibition/" + url
