import json
import re

import bs4

from helper.parse_helper import ParseInit


class TMCParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("p", {"class": "m-event-card__box-title"}).get_text()

    def get_date(self, *args, **kwargs) -> str:
        raw_date_string = self.item.find(
            "p", {"class": "m-event-card__box-bottom-date"}
        ).get_text()

        raw_date_string = raw_date_string.replace("-", "~")

        subbed_string = re.sub(r'(\(.\))', '', raw_date_string)

        return subbed_string

    def get_address(self, *args, **kwargs) -> str:
        return self.safe_get_text(
            self.item.find(
                "p", {"class": "m-event-card__box-bottom-location"}
            )
        )

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.find("div", {"class": "m-event-card__img"})["data-bg"]

    def get_source_url(self, *args, **kwargs) -> str:
        o_archive_frame__item_wrap = self.item.find(
            "div", {"class": "o-archive-frame__item-wrap"}
        )
        if this_a := o_archive_frame__item_wrap.find("a", {"class": "m-event-card"}):
            return this_a.get("href", "")
        else:
            data_session = o_archive_frame__item_wrap["data-session"]
            data_session_json = json.loads(data_session)
            link = data_session_json[-1].get("link")
        return link
