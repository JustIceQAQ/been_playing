import asyncio

import bs4
from app.museums.tncmmm.parse import TncMMMParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage

from typing import cast


class TncMMMRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TncMMMParse
    use_suffix_item_from_file_func = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.datong_63000060,
            fullname="臺灣新文化運動紀念館",
            code_name="TncMMM",
            external_link="https://tncmmm.gov.taipei/Content_List.aspx?n=2BF92E180FD68C1A",
            branch_coordinates=Coordinate(raw_coordinates="25.059502699444998, 121.51495546606633"),
            venue_type=VenueType.MEMORIAL,
        )

    async def fetch_response(self):
        headers = generate_headers(
            host="tncmmm.gov.taipei",
            referer="https://tncmmm.gov.taipei",
        )
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://tncmmm.gov.taipei/Content_List.aspx?n=2BF92E180FD68C1A",
                headers=headers,
            )
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("div.group-list.content a")


async def main():
    await TncMMMRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
