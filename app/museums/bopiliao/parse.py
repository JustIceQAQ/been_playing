import datetime

from helpers.parse_helper import ParseInit


class BoPiLiaoParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item["Name"]

    def get_date(self, *args, **kwargs) -> str | None:
        raw_start_date = self.item["StartDate"].replace("'", "")
        raw_end_date = self.item["EndDate"].replace("'", "")
        start_date = datetime.datetime.strptime(raw_start_date, "%y / %m / %d")
        end_date = datetime.datetime.strptime(raw_end_date, "%y / %m / %d")
        return f"{start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return f"https://www.bopiliao.taipei/upload/event_news/{self.item['Photo']}"

    def get_source_url(self, *args, **kwargs) -> str | None:
        return f"https://www.bopiliao.taipei/Event_News/Detail/{self.item['Id']}"
