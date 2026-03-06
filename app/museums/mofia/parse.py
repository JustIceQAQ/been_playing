from helpers.parse_helper import ParseInit


class MofiaParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("name")

    def get_date(self, *args, **kwargs) -> str | None:
        start_date = self.item.get("startDate").split("T")[0]
        end_date = self.item.get("endDate").split("T")[0]
        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        introduction = self.item.get("introduction")
        address = introduction.split("地點｜")
        if len(address) == 1:
            return None
        return address[1].split("\r\n\r\n")[0]

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://mofia.taichung.gov.tw/" + self.item.get("mainIcon")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        exhibit_id = self.item.get("id")
        return f"https://mofia.taichung.gov.tw/Exhibit/{exhibit_id}"
