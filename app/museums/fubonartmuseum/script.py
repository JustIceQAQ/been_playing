import asyncio

import bs4

from app.museums.fubonartmuseum.parse import FuBonArtMuseumParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GeoPoint
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
            location_code=Taiwan.taipei.xinyi_63000020,
            fullname="富邦美術館",
            code_name="FuBonArtMuseum",
            external_link="https://www.fubonartmuseum.org/Default",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.039545226356974, 121.57119466791848"),
                raw_coordinates="25.039545226356974, 121.57119466791848",
            ),
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
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await FuBonArtMuseumRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
