import datetime

from helpers.parse_helper import ParseInit


class OpenTixParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("source", {}).get("title", None)

    def get_date(self, *args, **kwargs) -> str:
        start_date_time: int | None = self.item.get("source", {}).get(
            "startDateTime", None
        )
        end_date_time: int | None = self.item.get("source", {}).get("endDateTime", None)
        date_time_string = ""
        if start_date_time is not None:
            date_time_string += datetime.date.fromtimestamp(
                start_date_time / 1e3
            ).isoformat()

        if end_date_time is not None:
            date_time_string += " ~ "
            date_time_string += datetime.date.fromtimestamp(
                end_date_time / 1e3
            ).isoformat()

        return date_time_string

    def get_address(self, *args, **kwargs) -> str:
        event_venues = self.item.get("source", {}).get("eventVenues", [])
        return ", ".join(
            [
                event_venue.get("name")
                for event_venue in event_venues
                if event_venue.get("name", None) is not None
            ]
        )

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.get("source", {}).get("imageUrl", None)

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return f'{target_domain}{self.item.get("source", {}).get("id", "")}'
