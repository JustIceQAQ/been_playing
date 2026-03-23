import bs4

from helpers.parse_helper import ParseInit


class NtMofaParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "caption"}).get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        date_str = ""
        if (date_obj := self.item.find("p", {"class": "activity-time"})) is not None:
            date_str = date_obj.get_text()
            if date_str:
                date_str = date_str.replace("時間：", "").strip()
                date_str = date_str.replace("日期:", "").strip()

                if "~" not in date_str:
                    date_str = date_str + " ~"

        return date_str

    def get_address(self, *args, **kwargs) -> str | None:
        runtime_address = None
        if address_element := self.item.find("p", {"class": "activity-season"}):
            if runtime_address := address_element.get_text():
                runtime_address = runtime_address.replace("地點：", "").replace("，", "、").strip()
        return runtime_address

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find(
            "img",
        ).get("src")

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.get("href")
