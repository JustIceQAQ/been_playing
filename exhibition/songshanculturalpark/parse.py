import bs4

from helper.parse_helper import ParseInit


class SongShanCulturalParkParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("span.row_rt > p.lv_h2").get_text()

    def get_date(self, *args, **kwargs) -> str:
        raw_date_string = self.item.select_one("span.row_rt > p.date.montsrt").get_text()
        raw_date_string = raw_date_string.replace("-", "~")
        return raw_date_string

    def get_address(self, *args, **kwargs) -> str:
        return "-"

    def get_figure(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.select_one("span.row_lt > img")["src"]
        )

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.select_one("span.row_rt > a")["href"]
        )
