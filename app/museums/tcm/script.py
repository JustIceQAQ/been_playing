import asyncio
from typing import cast

import bs4
import httpx

from app.museums.tcm.parse import TcmParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


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
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="22.987586370137066, 120.20828174089186"),
                raw_coordinates="22.987586370137066, 120.20828174089186",
            ),
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
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await TcmRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
