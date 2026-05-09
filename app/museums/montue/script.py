import asyncio

import bs4
import httpx
import logging
from app.museums.montue.parse import MoNTUEParse
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


class MoNTUERunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = MoNTUEParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.daan_63000030,
            fullname="北師美術館",
            code_name="MoNTUE",
            external_link="https://montue.ntue.edu.tw/",
            branch_coordinates=Coordinate(raw_coordinates="25.024774854666255, 121.54460696977063"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def sub_fetch_response(self, client: httpx.AsyncClient, url: str) -> str:
        response = await client.get(url)
        return response.text

    async def fetch_response(self):
        headers = generate_headers()
        urls = [
            "https://montue.ntue.edu.tw/exhibitions/",
            "https://montue.ntue.edu.tw/exhibitions-upcoming/",
        ]
        async with HttpxAsyncClient(headers=headers) as client:
            get_a_tasks = [self.sub_fetch_response(client, url) for url in urls]
            all_items_url = []
            get_a_results = await asyncio.gather(*get_a_tasks)
            for result in get_a_results:
                soup = BeautifulSoupTranslation().translation_to_object(result)
                divs = soup.find_all(
                    "div",
                    {"class": "ptsc pt-sc sc-slider exhibition-slider hide-title hide-mobile"},
                )
                for div in divs:
                    all_items_url.append(div.find("a").get("href"))
            if not all_items_url:
                logging.error("all_items_url data is %s", bool(all_items_url))
            get_items_context = [self.sub_fetch_response(client, item_url) for item_url in set(all_items_url)]
            get_items_context_results = await asyncio.gather(*get_items_context)
            if not get_items_context_results:
                logging.error("get_items_context_results data is %s", bool(all_items_url))
        return get_items_context_results

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        return parsed


async def main():
    await MoNTUERunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
