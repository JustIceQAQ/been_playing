from helpers.parse_helper import ParseInit


class MofiaParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        name = self.item.get("name")
        if name is None:
            return None
        return name

    def get_date(self, *args, **kwargs) -> str | None:
        start_date = self.item.get("startDate")
        if start_date is None:
            return None

        start_date = start_date.split("T")[0]

        end_date = self.item.get("endDate")
        if end_date is None:
            return start_date

        end_date = end_date.split("T")[0]
        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        introduction = self.item.get("introduction")
        if introduction is None:
            return None
        address = introduction.split("地點｜")
        if len(address) == 1:
            return None
        return address[1].split("\r\n\r\n")[0]

    def get_figure(self, *args, **kwargs) -> str | None:
        main_icon = self.item.get("mainIcon")
        if main_icon:
            return "https://mofia.taichung.gov.tw/" + main_icon

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        exhibit_id = self.item.get("id")
        if exhibit_id is None:
            return None
        return f"https://mofia.taichung.gov.tw/Exhibit/{exhibit_id}"
