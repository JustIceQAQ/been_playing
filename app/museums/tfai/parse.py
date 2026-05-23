from helpers.parse_helper import ParseInit


class TFAIParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("zhName")

    def get_date(self, *args, **kwargs) -> str | None:
        raw_start_date: str | None = self.item.get("startDate")
        raw_end_date: str | None = self.item.get("endDate")
        if raw_start_date is None:
            return None

        ok_start_date = raw_start_date.split("(")[0].replace(".", "-")

        if raw_end_date is None:
            return ok_start_date

        ok_end_date = raw_end_date.split("(")[0].replace(".", "-")
        return f"{ok_start_date} ~ {ok_end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.get("imgPath")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        detail = self.item.get("id")
        return f"https://www.tfai.org.tw/zh/program/detail/{detail}"
