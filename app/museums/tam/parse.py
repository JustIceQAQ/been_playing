from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class TAMParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.attributes.get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        raw_date = self.item.css_first("span.kf_imglist_time").text(strip=True)
        parts = raw_date.split("~")
        if len(parts) != 2:
            return None

        def roc_to_ad(roc_date: str) -> str:
            year, month, day = roc_date.strip().split("-")
            return f"{int(year) + 1911}-{month}-{day}"

        return f"{roc_to_ad(parts[0])} ~ {roc_to_ad(parts[1])}"

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.css_first("div.kf_imglist_map_marker").text(strip=True)

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://tm.ccl.ttct.edu.tw/" + self.item.css_first("img").attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://tm.ccl.ttct.edu.tw/" + self.item.attributes.get("href")
