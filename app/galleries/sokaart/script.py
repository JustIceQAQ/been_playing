import asyncio

import bs4

from app.galleries.sokaart.parse import SoKaArtParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class SoKaArtRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = SoKaArtParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="索卡藝術中心",
            code_name="SoKaArt",
            external_link="https://www.soka-art.com/tr",
            branch_coordinates=Coordinate(
                raw_coordinates="25.07961383080647, 121.56344961543039"
            ),
            venue_type=VenueType.GALLERY,
        )

    async def fetch_response(self):
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://soka-art.com/tr/exhibition/current?artist_area=5"
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div.exhibition-list-wrapper li.item")


async def main():
    await SoKaArtRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
