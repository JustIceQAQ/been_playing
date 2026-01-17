import asyncio

import bs4

from app.museums.huashan1914.parse import huashan1914Parse
from helpers.cache import NoneCache
import httpx
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate, ExhibitionItem
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3, get_asyncio_rate_limit


class HuaShan1914Runner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = huashan1914Parse
    use_suffix_item_from_url_auto = True
    use_suffix_item_from_file_func = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="華山1914文化創意產業園區",
            code_name="HuaShan1914",
            external_link="https://www.huashan1914.com/w/huashan1914/exhibition",
            branch_coordinates=Coordinate(
                google_map_place_id="ChIJbSTgI2WpQjQRcVwWB2cnyfE",
                raw_coordinates="25.044242402011122, 121.5292898083939",
            ),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        index = 1
        datasets = []
        async with HttpxAsyncClient() as client:
            while True:
                response = await client.get(
                    f"https://www.huashan1914.com/w/huashan1914/exhibition?index={index}",
                    headers=get_headers(),
                )
                dataset = bs4.BeautifulSoup(response.text, "html5lib").select(
                    "ul#event-ul li"
                )
                if dataset:
                    datasets.append(response.text)
                    index = index + 1
                else:
                    break
        return datasets

    async def fetch_parsed(self):
        items = []
        parsers: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        for parsed in parsers:
            sub_items = parsed.select("ul#event-ul li")
            items.extend(sub_items)
        return items

    async def fetch_items(self, *args, **kwargs):
        return await super().fetch_items(target_domain="https://www.huashan1914.com")

    async def _get_item_data(self, client: httpx.AsyncClient, item: ExhibitionItem):
        has_address_cache = await self.cache.aget(f"{item.UUID}-address")
        if has_address_cache:
            item.address = has_address_cache
            return
        response = await client.get(item.source_url)
        soup = self.translation().translation_to_object(response.text)
        exhibition_location = None
        a_elements = soup.select("div.address a")
        if a_elements:
            exhibition_location = ", ".join([a_element.get_text(strip=True) for a_element in a_elements])
        await self.cache.aset(f"{item.UUID}-address", exhibition_location, month_3())
        item.address = exhibition_location

    async def suffix_item_from_url_auto(self, items: list[ExhibitionItem]):
        asyncio_limit = get_asyncio_rate_limit(3, 30)
        headers = get_headers()
        async with HttpxAsyncClient(headers=headers) as client, asyncio_limit:
            tasks = [self._get_item_data(client, item) for item in items]
            await asyncio.gather(*tasks)


async def main():
    await HuaShan1914Runner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
