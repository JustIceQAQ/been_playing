import asyncio

import bs4

from app.galleries.cg1839.parse import CG1839Parse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3

from typing import cast


class CG1839Runner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = CG1839Parse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.daan_63000030,
            fullname="1839 當代藝廊",
            code_name="CG1839",
            external_link="https://www.1839cg.com/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.040566348234144, 121.55455459325458"),
                raw_coordinates="25.040566348234144, 121.55455459325458",
            ),
            venue_type=VenueType.GALLERY,
        )

    async def fetch_response(self):
        headers = generate_headers()
        all_items = []

        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.1839cg.com/")
            response.raise_for_status()

            await self.get_index_item(all_items, client, response)

            await self.get_current_item(all_items, client)

        return all_items

    async def get_current_item(self, all_items, client):
        current_response = await client.get("https://www.1839cg.com/current-exhibition")
        current_response.raise_for_status()
        current_p = BeautifulSoupTranslation().translation_to_object(current_response.text)
        current_responses = await asyncio.gather(
            *[client.get(a.get("href")) for a in current_p.select("p.has-text-align-center a")]
        )
        all_items.extend([current_response.text for current_response in current_responses])

    async def get_index_item(self, all_items, client, response):
        p = BeautifulSoupTranslation().translation_to_object(response.text)
        items_response = p.select("div.entry-content figure.wp-block-image a")[:3]
        responses = await asyncio.gather(*[client.get(item.get("href")) for item in items_response])
        all_items.extend([item_response.text for item_response in responses])

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        return parsed


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await CG1839Runner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
