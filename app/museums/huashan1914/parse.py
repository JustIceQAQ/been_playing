from helpers.parse_helper import ParseInit


class huashan1914Parse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item["article"]["default"]["title"]

    def get_date(self, *args, **kwargs) -> str | None:
        event_time = self.item["article"]["event_time"]
        start_date = event_time["start_date"].split("T")[0]
        end_date = event_time["end_date"].split("T")[0]
        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        aside = self.item["aside"]
        this_category_event_venues = aside["category_event_venue"]
        event_venue_data = kwargs.get("event_venue_data", {})
        return "/".join(
            event_venue_data[this_category_event_venue] for this_category_event_venue in this_category_event_venues
        )

    def get_figure(self, *args, **kwargs) -> str | None:
        event_content = self.item["article"]["event_content"]
        return event_content["hero_img"][0]["thumbnail_path"]

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        aside = self.item["aside"]
        this_category_event_categories = aside["category_event_category"]
        event_category_data = kwargs.get("event_category_data", {})
        return [
            event_category_data[this_category_event_category]
            for this_category_event_category in this_category_event_categories
        ]

    def get_source_url(self, *args, **kwargs) -> str | None:
        slug = self.item["article"]["default"]["slug"]
        return "{}{}".format("https://www.huashan1914.com/exhibition/", slug)
