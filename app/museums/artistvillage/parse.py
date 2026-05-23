from helpers.parse_helper import ParseInit


class ArtistVillageParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("post_title", None)

    def get_date(self, *args, **kwargs) -> str | None:
        start_date = self.item.get("start_date", None)
        end_date = self.item.get("end_date", None)
        if start_date and end_date:
            return f"{start_date} ~ {end_date}"

        if start_date:
            return start_date

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        pass

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        p = self.item.get("ID", None)
        if p:
            return f"https://www.artistvillage.org/event-detail.php?p={p}"
