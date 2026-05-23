from helpers.parse_helper import ParseInit

from selectolax.lexbor import LexborNode

from helpers.utils_helper import set_date, to_ad_year


class TyCgParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.attributes.get("title")

    def get_date(self, *args, **kwargs) -> str | None:
        marks = self.item.css("i.mark")
        if len(marks) == 2:
            datetime = marks[0].text(strip=True).replace("/", "-")
            start_date_str, end_date_str = datetime.split("~")
            sy, sm, sd = start_date_str.split("-")
            ey, em, ed = end_date_str.split("-")

            start_date = set_date(to_ad_year(int(sy)), int(sm), int(sd)).isoformat()
            end_date = set_date(to_ad_year(int(ey)), int(em), int(ed)).isoformat()

            return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        marks = self.item.css("i.mark")
        if len(marks) == 2:
            return marks[1].text(strip=True)

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.css_first("img").attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        href = self.item.attributes.get("href")
        if href is None:
            return None
        return "https://wem.tycg.gov.tw/" + href
