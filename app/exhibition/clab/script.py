import bs4
import httpx

from app.exhibition.clab.parse import CLabParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import date_now, month_3


class CLabRunner(RunnerInit):
    """臺灣當代文化實驗場 C-LAB"""

    translation = BeautifulSoupTranslation
    use_parse = CLabParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="台灣當代文化實驗場C-Lab",
            code_name="CLab",
            external_link="https://clab.org.tw/events/",
        )

    async def fetch_response(self):
        today = date_now()
        filter_year = today.year
        filter_month = today.month
        target_url_template = (
            "https://clab.org.tw/events/?"
            "event_category=exhibition"
            "&filter_year={filter_year}"
            "&filter_month={filter_month}"
        )
        target_url = target_url_template.format(
            filter_year=filter_year, filter_month=filter_month
        )
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(target_url, headers=get_header())
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.find_all("div", {"data-aos": "-block-line"})
