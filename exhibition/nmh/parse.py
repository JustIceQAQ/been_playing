import bs4

from helper.parse_helper import ParseInit


class NMHParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("div", {"class": "caption"}).get_text().strip()

    def get_date(self, *args, **kwargs) -> str:
        date_str = self.item.find("p", {"class": "activity-time"}).get_text()
        if date_str:
            date_str = date_str.replace("時間：", "").strip()
        return date_str

    def get_address(self, *args, **kwargs) -> str:
        runtime_address = None
        if address_element := self.item.find("p", {"class": "activity-season"}):
            if runtime_address := address_element.get_text():
                runtime_address = runtime_address.replace("場地：", "").strip()
        return runtime_address

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.find("img").get("src", None)

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.find("a",
                              {"class": "div", "target": "_blank"}).get("href", None)
