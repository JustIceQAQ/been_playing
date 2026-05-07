import asyncio

import bs4

from app.museums.ntnu_art_museum.parse import NTNUArtMuseumParse
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


class NTNUArtMuseumRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NTNUArtMuseumParse
    use_suffix_item_from_file_func: bool = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.da_an_63000030,
            fullname="師大美術館",
            code_name="NTNUArtMuseum",
            external_link="https://www.artmuse.ntnu.edu.tw/index.php/current_exhibit/",
            branch_coordinates=Coordinate(raw_coordinates="25.027981327647616, 121.53016316977069"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="www.artmuse.ntnu.edu.tw")
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.artmuse.ntnu.edu.tw/index.php/current_exhibit/")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        items = parsed.select("figcaption")
        return [item.parent for item in items]


async def main():
    await NTNUArtMuseumRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
