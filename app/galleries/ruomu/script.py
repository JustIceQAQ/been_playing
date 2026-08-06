import asyncio
from typing import cast

import bs4

from app.galleries.ruomu.parse import RuoMuParse
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class RuoMuRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = RuoMuParse
    retry_on_empty = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.daan_63000030,
            fullname="若木藝廊",
            code_name="RuoMu",
            external_link="https://www.ruomugallery.com/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.033909532791032, 121.52358387976376"),
                raw_coordinates="25.033909532791032, 121.52358387976376",
            ),
            venue_type=VenueType.GALLERY,
        )

    async def fetch_response(self):
        headers = generate_headers(
            need_upgrade_insecure_requests=True,
            host="www.ruomugallery.com",
        )
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.ruomugallery.com/exhibitions/")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("#exhibitions-grid-current li")


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await RuoMuRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
