import asyncio

import bs4

from app.museums.alien.parse import AlienParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3

from typing import cast


class AlienRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = AlienParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.kaohsiung.gushan_64000020,
            fullname="金馬賓館當代美術館",
            code_name="Alien",
            external_link="https://www.alien.com.tw/u/zh-tw/list/exhibitions",
            branch_coordinates=Coordinate(raw_coordinates="22.627619441196142, 120.278842832973"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            referer="https://www.alien.com.tw/u/zh-tw/pages/Plan_Your_Visit",
            host="www.alien.com.tw",
        )
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.alien.com.tw/u/zh-tw/list/exhibitions")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        list_content_area = parsed.select("div.listContentArea")
        return list_content_area[:11]


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image.none.helper import NoneImage

    await AlienRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
