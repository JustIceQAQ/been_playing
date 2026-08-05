import asyncio
from typing import cast

import bs4

from app.museums.chipolin.parse import ChiPoLinParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class ChiPoLinRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = ChiPoLinParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.new_taipei.tamsui_65000100,
            fullname="齊柏林空間",
            code_name="ChiPoLin",
            external_link="https://www.chipolin.org/exhibition",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.17294603618085, 121.43711272744605"),
                raw_coordinates="25.17294603618085, 121.43711272744605",
            ),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.chipolin.org/exhibition")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.find_all("li", {"class": "exhibition__item"})


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await ChiPoLinRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
