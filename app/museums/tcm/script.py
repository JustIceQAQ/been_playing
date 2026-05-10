import asyncio

import bs4
import httpx

from app.museums.tcm.parse import TcmParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3

from typing import cast


class TcmRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TcmParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.tainan.west_central_67000370,
            fullname="臺南市立博物館",
            code_name="Tcm",
            external_link="https://tcm.tainan.gov.tw/permanent",
            branch_coordinates=Coordinate(raw_coordinates="22.987586370137066, 120.20828174089186"),
            venue_type=VenueType.MUSEUM,
        )

    async def sub_client(self, client: httpx.AsyncClient, url: str):
        response = await client.get(url)
        response.raise_for_status()
        return response.text

    async def fetch_response(self):
        headers = generate_headers()
        urls = [
            "https://tcm.tainan.gov.tw/permanent",
            "https://tcm.tainan.gov.tw/special",
        ]
        async with HttpxAsyncClient(headers=headers) as client:
            responses = await asyncio.gather(*[self.sub_client(client, url) for url in urls])
        return responses

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        items = []
        for parse in parsed:
            items.extend(parse.select("div.content > div.row > div"))
        return items


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImage

    await TcmRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
