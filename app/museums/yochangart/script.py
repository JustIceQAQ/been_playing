import asyncio
from typing import cast

import bs4

from app.museums.yochangart.parse import YoChangArtParse
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class YoChangArtRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = YoChangArtParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.new_taipei.banqiao_65000010,
            fullname="有章藝術博物館",
            code_name="YoChangArt",
            external_link="https://museum.ntua.edu.tw/c001.asp",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.006981532547897, 121.44882905627831"),
                raw_coordinates="25.006981532547897, 121.44882905627831",
            ),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://museum.ntua.edu.tw/c001.asp")
            response.raise_for_status()
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("div.work_item")


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await YoChangArtRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
