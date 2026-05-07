import asyncio

import bs4

from app.museums.fubonartmuseum.parse import FuBonArtMuseumParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3

from typing import cast


class FuBonArtMuseumRunner(RunnerInit):
    """富邦美術館"""

    translation = BeautifulSoupTranslation
    use_parse = FuBonArtMuseumParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.xin_yi_63000020,
            fullname="富邦美術館",
            code_name="FuBonArtMuseum",
            external_link="https://www.fubonartmuseum.org/Default",
            branch_coordinates=Coordinate(raw_coordinates="25.039545226356974, 121.57119466791848"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        async with HttpxAsyncClient(headers=generate_headers()) as client:
            response = await client.get(
                "https://www.fubonartmuseum.org/Default",
            )
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("div#homepage-swiper-exhibitions > div.swiper-wrapper > div")


async def main():
    await FuBonArtMuseumRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
