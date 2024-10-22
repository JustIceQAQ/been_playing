import bs4
import cssutils

from helper.parse_helper import ParseInit


class MWRParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("div.title > a").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.select_one("div.date").get_text()

    def get_address(self, *args, **kwargs) -> str:
        return "-"

    def get_figure(self, *args, **kwargs) -> str:
        dev_style = self.item.select_one("div.imgBox > a > div.img").get("style")
        style = cssutils.parseStyle(dev_style)

        return (
            url.replace("url(", "")[:-1].replace('"', "")
            if (url := style["background-image"])
            else "-"
        )

    def get_source_url(self, *args, **kwargs) -> str:
        pre_path = "https://www.mwr.org.tw/{}"
        return pre_path.format(self.item.select_one("div.title > a").get("href"))
