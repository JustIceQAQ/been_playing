import asyncio

import bs4

from app.museums.clab.parse import CLabParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3, get_current_and_previous_month


class CLabRunner(RunnerInit):
    """臺灣當代文化實驗場 C-LAB"""

    translation = BeautifulSoupTranslation
    use_parse = CLabParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="台灣當代文化實驗場 C-Lab",
            code_name="CLab",
            external_link="https://clab.org.tw/events/",
            branch_coordinates=Coordinate(raw_coordinates="25.039263447268308, 121.53884705257425"),
        )

    async def fetch_response(self):
        current_period, previous_period = get_current_and_previous_month()

        target_url_template = (
            "https://clab.org.tw/events/?"
            "event_category="
            "&filter_year={filter_year}"
            "&filter_month={filter_month}"
        )

        target_url = target_url_template.format(
            filter_year=current_period[0], filter_month=current_period[1]
        )
        async with HttpxAsyncClient() as client:
            responses = await asyncio.gather(
                client.get(
                    target_url_template.format(
                        filter_year=current_period[0],
                        filter_month=current_period[1]
                    ), headers=get_headers()
                ),
                client.get(
                    target_url_template.format(
                        filter_year=previous_period[0],
                        filter_month=previous_period[1]
                    ), headers=get_headers()
                ),

            )
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parseds: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        datas = []
        for parsed in parseds:
            datas.extend(parsed.find_all("div", {"data-aos": "-block-line"}))
        return datas


async def main():
    await CLabRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
