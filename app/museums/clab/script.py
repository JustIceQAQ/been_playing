import asyncio
from typing import cast

import bs4

from app.museums.clab.parse import CLabParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3, get_date


class CLabRunner(RunnerInit):
    """臺灣當代文化實驗場 C-LAB"""

    translation = BeautifulSoupTranslation
    use_parse = CLabParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.daan_63000030,
            fullname="台灣當代文化實驗場 C-Lab",
            code_name="CLab",
            external_link="https://clab.org.tw/events/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.039263447268308, 121.53884705257425"),
                raw_coordinates="25.039263447268308, 121.53884705257425",
            ),
            venue_type=VenueType.ART_VILLAGE,
        )

    async def fetch_response(self):
        current_period, previous_period = get_date.current_and_previous_period

        target_url_template = (
            "https://clab.org.tw/events/?" "event_category=" "&filter_year={filter_year}" "&filter_month={filter_month}"
        )
        headers = generate_headers()

        async with HttpxAsyncClient(headers=headers) as client:
            responses = await asyncio.gather(
                client.get(
                    target_url_template.format(filter_year=current_period[0], filter_month=current_period[1]),
                ),
                client.get(
                    target_url_template.format(filter_year=previous_period[0], filter_month=previous_period[1]),
                ),
            )
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parseds = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        datas = []
        for parsed in parseds:
            datas.extend(parsed.find_all("div", {"data-aos": "-block-line"}))
        return datas


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await CLabRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
