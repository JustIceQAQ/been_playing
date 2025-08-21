from helpers.parse_helper import ParseInit


class PactParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item["Title"]

    def get_date(self, *args, **kwargs) -> str | None:
        start_date = self.item.get("PublishDate", None)
        if start_date is None:
            return None
        start_date = start_date.replace("/", "-")
        end_date = self.item.get("EventEndDate", None)
        if end_date is None:
            return start_date

        end_date = end_date.replace("/", "-")

        return start_date + " ~ " + end_date

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item["PlaceName"]

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://www.pact.taipei/upload/{}".format(self.item["ImageFileName"])

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.pact.taipei/exhibitionCT.aspx?id={}".format(self.item["Id"])
