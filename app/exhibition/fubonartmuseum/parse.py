import datetime

import bs4

from helpers.parse_helper import ParseInit


class FuBonArtMuseumParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        raw_text = self.item.select_one(".info_title").get_text()
        return raw_text.strip()

    def get_figure(self, *args, **kwargs) -> str:
        img = self.item.select_one("div.fb-photo-frame > img")
        return img["src"]

    def get_address(self, *args, **kwargs) -> str:
        datas = self.item.select("div.card_info > div.info_group > p.font-body")
        if len(datas) == 1:
            raw_text = datas[0].text.strip()
            if "." not in raw_text:
                return raw_text
        else:
            for data in datas:
                raw_text = data.text.strip()
                if "." not in raw_text:
                    return raw_text

        return ""

    def chech_is_date(self, data: bs4.element.Tag) -> str:
        now_year = datetime.datetime.now().year
        raw_text = data.text.strip()
        if "." in raw_text and "-" in raw_text:
            raw_start_date, raw_end_date = raw_text.split("-")
            this_raw_start_year = None
            this_raw_start_month = None

            if len(start_date_split := raw_start_date.split(".")) == 3:
                raw_start_year, raw_start_month, raw_day = start_date_split
                start_date = datetime.date(
                    int(raw_start_year),
                    int(raw_start_month),
                    int(raw_day),
                )
                this_raw_start_month = int(raw_start_month)
                this_raw_start_year = int(raw_start_year)
            else:
                raw_start_month, raw_day = start_date_split
                start_date = datetime.date(
                    int(now_year),
                    int(raw_start_month),
                    int(raw_day),
                )
                this_raw_start_month = int(raw_start_month)
                this_raw_start_year = int(now_year)

            if len(end_date_split := raw_end_date.split(".")) == 3:
                raw_year, raw_month, raw_day = end_date_split
                end_date = datetime.date(
                    int(raw_year),
                    int(raw_month),
                    int(raw_day),
                )
            else:
                raw_end_month, raw_day = end_date_split

                use_year = (
                    (this_raw_start_year + 1)
                    if this_raw_start_month > int(raw_end_month)
                    else this_raw_start_year
                )
                end_date = datetime.date(
                    int(use_year),
                    int(raw_end_month),
                    int(raw_day),
                )
            return f"{start_date.isoformat()} ~ {end_date.isoformat()}"
        return ""

    def get_date(self, *args, **kwargs) -> str:
        datas = self.item.select("div.card_info > div.info_group > p.font-body")
        cooked_string = ""
        if len(datas) == 1:
            cooked_string = self.chech_is_date(datas[0])
        else:
            for data in datas:
                if (cooked_string := self.chech_is_date(data)) != "":
                    return cooked_string

        return cooked_string

    def get_source_url(self, *args, **kwargs) -> str:
        a = self.item.find("a", {"class": "fb-exhibition-card"})
        return f"https://www.fubonartmuseum.org{a['href']}"
