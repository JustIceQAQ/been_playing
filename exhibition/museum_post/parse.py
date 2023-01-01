import bs4

from helper.parse_helper import ParseInit


class MuseumPostParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("h3").get_text()

    def get_date(self, *args, **kwargs) -> str:
        date_value = "-"
        if runtime_value := self.item.find("div", {"class": "ex_date"}):
            date_value = runtime_value.get_text().replace("日期：", "").strip()
        return date_value

    def get_address(self, *args, **kwargs) -> str:
        address_value = "-"
        if runtime_value := self.item.find("div", {"class": "ex_place"}):
            address_value = runtime_value.get_text().replace("地點：", "").strip()
        return address_value

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.find("img").get("src")

    def get_source_url(self, *args, **kwargs) -> str:
        pre_url = "https://museum.post.gov.tw/post/Postal_Museum/museum/{}"
        return pre_url.format(
            self.item.find("div", {"class": "textWrap"}).find("a").get("href")
        )
