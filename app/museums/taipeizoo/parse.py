import html
import re

from helpers.parse_helper import ParseInit


_MIN_ROC_YEAR = 95  # ROC 95 = 2006，避免誤抓內文中的非展期年份數字


def _roc_to_ad(year: str, month: str, day: str) -> str | None:
    roc_year = int(year)
    if roc_year < _MIN_ROC_YEAR:
        return None
    return f"{roc_year + 1911}-{int(month):02d}-{int(day):02d}"


class TaipeiZooParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.get("title")

    def _content(self) -> str:
        raw = self.item.get("內容", "") or ""
        return html.unescape(raw)

    def get_date(self, *args, **kwargs) -> str | None:
        content = self._content()

        # "114年12月1日至115年11月30日"
        range_match = re.search(
            r"(\d{2,3})年(\d{1,2})月(\d{1,2})日[至到](\d{2,3})年(\d{1,2})月(\d{1,2})日",
            content,
        )
        if range_match:
            start = _roc_to_ad(range_match.group(1), range_match.group(2), range_match.group(3))
            end = _roc_to_ad(range_match.group(4), range_match.group(5), range_match.group(6))
            if start and end:
                return f"{start} ~ {end}"

        # "即日起至114年12月1日"
        immediate_match = re.search(
            r"即日起[至到](\d{2,3})年(\d{1,2})月(\d{1,2})日",
            content,
        )
        if immediate_match:
            end = _roc_to_ad(immediate_match.group(1), immediate_match.group(2), immediate_match.group(3))
            if end:
                return f"~ {end}"

        # "114年4月1日起"
        start_match = re.search(
            r"(\d{2,3})年(\d{1,2})月(\d{1,2})日起",
            content,
        )
        if start_match:
            start = _roc_to_ad(start_match.group(1), start_match.group(2), start_match.group(3))
            if start:
                return f"{start} ~"

        return None

    def get_address(self, *args, **kwargs) -> str | None:
        content = self._content()

        # "地點：臺北市立動物園昆蟲館"（排除 "展區地點："）
        match = re.search(r"(?<!展區)地點：([^\n]+)", content)
        if match:
            addr = (
                re.split(
                    r"特展網站|主題網站|兌換時間|特展簡介|展覽主題|特展主題|主辦單位|指導單位|展覽時間|系列活動|開幕活動|開幕時間|活動：|「",
                    match.group(1),
                )[0]
                .rstrip("。、 ")
                .strip()
            )
            if addr:
                return addr

        return "臺北市立動物園"

    def get_figure(self, *args, **kwargs) -> str | None:
        images = self.item.get("相關圖片")
        if not images:
            return None
        return images[0].get("url")

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        return ["特展"]

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.get("Source")
