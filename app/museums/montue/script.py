import asyncio
from typing import cast

import bs4

from app.museums.montue.parse import MoNTUEParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


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
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.024774854666255, 121.54460696977063"),
                raw_coordinates="25.024774854666255, 121.54460696977063",
            ),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def sub_fetch_response(self, client, url: str) -> str:
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
                if soup is None:
                    continue
                divs = soup.find_all(
                    "div",
                    {"class": "ptsc pt-sc sc-slider exhibition-slider hide-title hide-mobile"},
                )
                for div in divs:
                    all_items_url.append(div.find("a").get("href"))
            get_items_context = [self.sub_fetch_response(client, item_url) for item_url in set(all_items_url)]
            get_items_context_results = await asyncio.gather(*get_items_context)
        return get_items_context_results

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        return parsed


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await MoNTUERunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
