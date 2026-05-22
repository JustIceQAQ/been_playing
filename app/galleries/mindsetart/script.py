import asyncio

import bs4

from app.galleries.mindsetart.parse import MindSetArtParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3

from typing import cast


class MindSetArtRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = MindSetArtParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.neihu_63000100,
            fullname="安卓藝術",
            code_name="MindSetArt",
            external_link="https://www.art-msac.com/",
            branch_coordinates=Coordinate(raw_coordinates="25.086444326900594, 121.56138806256338"),
            venue_type=VenueType.GALLERY,
        )

    async def fetch_response(self):
        headers = generate_headers(host="www.art-msac.com")
        cookies = generate_cookies(other_cookies={"splash_screen_disabled": "true"})
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.art-msac.com/exhibitions/", cookies=cookies)
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        lis = parsed.select("div#exhibitions-grid-container li")
        return lis[:-1]


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await MindSetArtRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
