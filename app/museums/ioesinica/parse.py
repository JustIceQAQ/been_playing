from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class IOESinicaParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.attributes.get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        date = self.item.css_first("span.infos").text(strip=True).replace("~", " ~ ")
        if "~" not in date:
            date = date + " ~"
        return date

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        style = self.item.css_first("div.icr_img").attributes.get("style")
        path = style.split("url('")[1][:-2]
        return "https://www.ioe.sinica.edu.tw" + path

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.ioe.sinica.edu.tw" + self.item.attributes.get("href")
