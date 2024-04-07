import bs4
import cssutils

from helper.parse_helper import ParseInit


class NCPIParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.get("title")

    def get_date(self, *args, **kwargs) -> str:
        raw_date_string = self.item.select_one("div.info-box > div.date").get_text()
        raw_date_string = raw_date_string.replace("-", "~")
        raw_date_string = raw_date_string.replace(".", "-")
        return raw_date_string

    def get_address(self, *args, **kwargs) -> str:
        return self.item.select_one("div.info-box > div.location").get_text()

    def get_figure(self, *args, **kwargs) -> str:
        dev_style = self.item.find("div", {"class": "img"}).get("style")
        style = cssutils.parseStyle(dev_style)

        return (
            url.replace("url(", "")[:-1].replace('"', "").replace(' ', "%20")
            if (url := style["background-image"])
            else "-"
        )

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(target_domain, self.item.get("href"))
