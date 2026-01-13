import bs4
import cssutils

from helpers.parse_helper import ParseInit


class MwrParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("div.title > a").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.select_one("div.date").get_text()

    def get_address(self, *args, **kwargs) -> str | None:
        return None

    def get_figure(self, *args, **kwargs) -> str:
        dev_style = self.item.select_one("div.imgBox > a > div.img").get("style")
        style = cssutils.parseStyle(dev_style)

        return (
            url.replace("url(", "")[:-1].replace('"', "")
            if (url := style["background-image"])
            else "-"
        )

    def get_source_url(self, *args, **kwargs) -> str | None:
        pre_path = "https://www.mwr.org.tw{}"
        href = self.item.select_one("div.title > a").get("href")
        if href is None:
            return None
        if "http://" in href or "https://" in href:
            return href
        return pre_path.format(self.item.select_one("div.title > a").get("href"))
