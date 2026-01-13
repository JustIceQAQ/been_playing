import datetime
import re

from helpers.parse_helper import ParseInit
from helpers.utils_helper import TAIWAN_TIMEZONE


class NtcArtMuseumParse(ParseInit):
    def __init__(self, item: dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.get("ExName")

    def get_date(self, *args, **kwargs) -> str | None:
        pattern = r"\((\d+)\)"
        ex_date_st: str | None = self.item.get("ExDateSt", None)
        ex_date_en: str | None = self.item.get("ExDateEn", None)

        if ex_date_st is None:
            return None

        ex_date_st_match = re.search(pattern, ex_date_st)
        ex_date_st_formatted_date = None
        if ex_date_st_match:
            ex_date_st_timestamp_str = ex_date_st_match.group(1)
            ex_date_st_timestamp_ms = int(ex_date_st_timestamp_str) / 1000
            ex_date_st_object_utc = datetime.datetime.fromtimestamp(
                ex_date_st_timestamp_ms, TAIWAN_TIMEZONE
            )
            ex_date_st_formatted_date = ex_date_st_object_utc.strftime("%Y-%m-%d")

        if ex_date_en is None:
            return ex_date_st_formatted_date

        ex_date_en_match = re.search(pattern, ex_date_en)
        ex_date_en_formatted_date = None
        if ex_date_en_match:
            ex_date_en_timestamp_str = ex_date_en_match.group(1)
            ex_date_en_timestamp_ms = int(ex_date_en_timestamp_str) / 1000
            ex_date_en_object_utc = datetime.datetime.fromtimestamp(
                ex_date_en_timestamp_ms, TAIWAN_TIMEZONE
            )
            ex_date_en_formatted_date = ex_date_en_object_utc.strftime("%Y-%m-%d")

        return ex_date_st_formatted_date + " ~ " + ex_date_en_formatted_date

    def get_address(self, *args, **kwargs) -> str:
        return self.item.get("ExLocationTextTW").split("–")[1].strip()

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        ex_tag_set_text_tw: str | None = self.item.get("ExTagSetTextTW", None)
        if ex_tag_set_text_tw is None:
            return None
        return ex_tag_set_text_tw.split(", ")

    def get_figure(self, *args, **kwargs) -> str:
        return "https://admin.ntcart.museum/Upload/" + self.item.get("ExListImg")

    def get_source_url(self, *args, **kwargs) -> str:
        ex_no = self.item.get("ExNo")
        return "https://ntcart.museum/exhibition_content.aspx?id=" + ex_no
