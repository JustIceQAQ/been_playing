import bs4

from helpers.parse_helper import ParseInit


class NMTLParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return (
            self.item.find("div", {"class": "caption"})
            .find("span")
            .get_text(strip=True)
        )

    def get_date(self, *args, **kwargs) -> str | None:
        label = self.item.find("div", {"class": "label"})
        lis = label.find_all("li")
        if not lis:
            return None
        activity_time = label.find("p", {"class": "activity-time"})
        if activity_time is None:
            return None
        return activity_time.get_text(strip=True).replace("日期：", "").strip()

    def get_address(self, *args, **kwargs) -> str | None:
        label = self.item.find("div", {"class": "label"})
        lis = label.find_all("li")
        if not lis:
            return None
        activity_season = label.find("p", {"class": "activity-season"})
        if activity_season is None:
            return None

        raw_address = activity_season.get_text(strip=True).replace("地點：", "").strip()
        if "-" in raw_address:
            ok_address = raw_address[raw_address.index("-") + 1 :]
        elif "─" in raw_address:
            ok_address = raw_address[raw_address.index("─") + 1 :]
        elif "國立臺灣文學館" in raw_address:
            ok_address = raw_address.split("國立臺灣文學館")[-1]
        else:
            ok_address = raw_address

        return ok_address

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.find("a").get("href")
