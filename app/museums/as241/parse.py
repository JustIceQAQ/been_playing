from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class AS241Parse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.css_first("a").attributes.get("title").split("]")[-1]

    def get_date(self, *args, **kwargs) -> str | None:
        list_date_activity = self.item.css_first("div.list_date_activity").text(strip=True)

        def roc_to_ad(roc_date: str) -> str:
            year, month, day = roc_date.strip().split("-")
            return f"{int(year) + 1911}-{month}-{day}"

        if "~" in list_date_activity:
            start, end = list_date_activity.split("~")
            return f"{roc_to_ad(start)} ~ {roc_to_ad(end)}"
        return roc_to_ad(list_date_activity)

    def get_address(self, *args, **kwargs) -> str | None:
        return "新竹241藝術空間"

    def get_figure(self, *args, **kwargs) -> str | None:
        pass

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://culture.hccg.gov.tw/ch/" + self.item.css_first("a").attributes.get("href")
