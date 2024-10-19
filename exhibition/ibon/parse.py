import datetime

from helper.parse_helper import ParseInit


class IBonParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.get("title")

    def get_date(self, *args, **kwargs) -> str:
        runtime_date = []

        start_date_millisecond = self.item.get("startDate", None)
        if start_date_millisecond is not None:
            start_date = datetime.datetime.fromtimestamp(start_date_millisecond // 1000)
            runtime_date.append(start_date.date().isoformat())

        end_date_millisecond = self.item.get("endDate", None)
        if end_date_millisecond is not None:
            end_date = datetime.datetime.fromtimestamp(end_date_millisecond // 1000)
            runtime_date.append(end_date.date().isoformat())

        return " ~ ".join(runtime_date)

    def get_address(self, *args, **kwargs) -> str:
        return self.item.get("displayAddress")

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.get("coverUrl")

    def get_source_url(self, *args, **kwargs) -> str:
        return "https://tour.ibon.com.tw/event/{}".format(self.item.get("id"))
