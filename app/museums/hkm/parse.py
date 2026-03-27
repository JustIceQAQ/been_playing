from helpers.parse_helper import ParseInit

from selectolax.lexbor import LexborNode
import re


class HKMParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.css_first("span.field--name-title").text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        node = self.item.css_first(".exhibition-date")
        for span in node.css("span"):
            span.decompose()
        text = node.text(strip=True)
        dates = re.findall(r"\d{4}\.\d{2}\.\d{2}", text)
        start_date = dates[0].replace(".", "-")
        end_date = dates[1].replace(".", "-")

        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        img = self.item.css_first("img")
        return "https://hkm.pccu.edu.tw" + img.attributes.get("data-src")

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://hkm.pccu.edu.tw" + self.item.attributes.get("about")
