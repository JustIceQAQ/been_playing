from helpers.parse_helper import ParseInit


class TaiwanHistoricaParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("主題")

    def get_date(self, *args, **kwargs) -> str | None:
        start_date = self.item.get("展覽開始日期")
        end_date = self.item.get("展覽結束日期")
        if start_date is None:
            return None

        if end_date is None:
            return start_date

        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.get("展覽地點")

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.get("FirstPicFullPath")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        url_path = self.item.get("Path")
        if url_path is None:
            return None
        return "https://www.th.gov.tw" + url_path
