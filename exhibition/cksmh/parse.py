import bs4
from typing import Optional
from helper.parse_helper import ParseInit


class CKSMHParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a > div.h3").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > span.date").get_text().replace("/", "-")

    def get_address(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > span.location").get_text()

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a > span > img")["src"]

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a")["href"]


class CKSMHParse2(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> Optional[str]:
        if (caption := self.item.select_one("div.essay > div.caption")) is not None:
            return caption.get_text()
        return None

    def get_date(self, *args, **kwargs) -> Optional[str]:
        if (activity_time := self.item.select_one("p.activity-time")) is not None:
            return activity_time.get_text().replace("日期 : ", "")

    def get_address(self, *args, **kwargs) -> Optional[str]:
        if (activity_season := self.item.select_one("p.activity-season")) is not None:
            return activity_season.get_text().replace("地點 : ", "")
        return None

    def get_figure(self, *args, **kwargs) -> Optional[str]:
        if (img := self.item.select_one("div.img > span > img")) is not None:
            return img["src"]
        return None

    def get_source_url(self, *args, **kwargs) -> Optional[str]:
        if (a := self.item.select_one("a.div-activity")) is not None:
            return a["href"]
        return None
