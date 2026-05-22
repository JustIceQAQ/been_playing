from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit
from helpers.utils_helper import get_roc_era_to_ad, set_date


class CZHParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        title = self.item.css_first("a").attributes.get("title")
        return title.replace("【彰化藝術館】", "").strip()

    def get_date(self, *args, **kwargs) -> str | None:
        raw_start_date = self.item.css_first("td[data-title='活動日期(起)']")
        raw_end_date = self.item.css_first("td[data-title='活動日期(迄) ']")

        if raw_start_date is None:
            return None

        span_start_date = raw_start_date.css_first("span").text(strip=True).split(" ")[0]
        sy, sm, sd = span_start_date.split("-")
        start_date = set_date(get_roc_era_to_ad(int(sy)), int(sm), int(sd)).isoformat()

        if raw_end_date is None:
            return start_date

        span_end_date = raw_end_date.css_first("span").text(strip=True).split(" ")[0]
        ey, em, ed = span_end_date.split("-")
        end_date = set_date(get_roc_era_to_ad(int(ey)), int(em), int(ed)).isoformat()

        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        pass

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        source_url = self.item.css_first("a").attributes.get("href")
        return "https://www.bocach.gov.tw/" + source_url
