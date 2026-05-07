import asyncio

import bs4

from app.museums.yochangart.parse import YoChangArtParse
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


class YoChangArtRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = YoChangArtParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.new_taipei.ban_qiao_65000010,
            fullname="有章藝術博物館",
            code_name="YoChangArt",
            external_link="https://museum.ntua.edu.tw/c001.asp",
            branch_coordinates=Coordinate(raw_coordinates="25.006981532547897, 121.44882905627831"),
            venue_type=VenueType.MUSEUM,
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
    await YoChangArtRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
