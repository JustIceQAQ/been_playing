import re

from helpers.parse_helper import ParseInit


from selectolax.lexbor import LexborNode


class HcccArtParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.css_first("a").attributes.get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        nodes = self.item.css(".date-item")
        dates = [n.text(strip=True) for n in nodes if n.text(strip=True) != "至"]
        if len(dates) < 2:
            return None

        def roc_to_ad(roc_date: str) -> str:
            year, month, day = roc_date.split("-")
            return f"{int(year) + 1911}-{month}-{day}"

        return f"{roc_to_ad(dates[0])} ~ {roc_to_ad(dates[1])}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        node = self.item.css_first(".bg")
        if not node:
            return None
        style = node.attributes.get("style", "")
        match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
        return match.group(1) if match else None

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.css_first("a").attributes.get("href")
