import bs4

from helpers.parse_helper import ParseInit

from pydantic import BaseModel, Field


class PathQuery(BaseModel):
    n: int
    sms: int
    csn: int = Field(alias="_CSN")


csn_list = [2446, 4479, 4477]

main_build: list[PathQuery] = [
    PathQuery(n=5472, sms=13389, _CSN=csn) for csn in csn_list
]

natural_history_branch: list[PathQuery] = [
    PathQuery(n=5473, sms=13389, _CSN=csn) for csn in csn_list
]

nanmen_branch: list[PathQuery] = [
    PathQuery(n=5474, sms=13389, _CSN=csn) for csn in csn_list
]

railway_department_park: list[PathQuery] = [
    PathQuery(n=5478, sms=13389, _CSN=csn) for csn in csn_list
]

other_venue: list[PathQuery] = [
    PathQuery(n=5477, sms=13389, _CSN=csn) for csn in csn_list
]

all_branch: list[list[PathQuery]] = [
    main_build,
    natural_history_branch,
    nanmen_branch,
    railway_department_park,
    other_venue,
]


class NtmParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("div.caption > span").get_text()

    def get_date(self, *args, **kwargs) -> str | None:
        if (
            result := self.safe_get_text(self.item.select_one("p.activity-time"))
        ) is not None:
            return result.replace("日期：", "").strip()
        return None

    def get_address(self, *args, **kwargs) -> str | None:
        if (
            result := self.safe_get_text(self.item.select_one("p.activity-season"))
        ) is not None:
            return result.replace("地點：", "").strip()
        return None

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.select_one("img")["src"]

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("a")["href"]
