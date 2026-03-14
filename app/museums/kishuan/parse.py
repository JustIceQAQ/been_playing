from selectolax.lexbor import LexborNode
from helpers.parse_helper import ParseInit


class KiShuAnParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        title = self.item.css_first("h3.title")
        return title.text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        date = self.item.css_first("div.date")
        return date.text(strip=True).replace("至", " ~ ")

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        img = self.item.css_first("img.img-responsive")
        return "https://kishuan.org.tw" + img.attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        a = self.item.css_first("a")
        return "https://kishuan.org.tw/" + a.attributes.get("href")
