import asyncio
import httpx
import bs4
from app.museums.nrm.parse import NrmParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate, ExhibitionItem
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3, get_asyncio_rate_limit

from typing import cast


class NrmRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NrmParse
    use_suffix_item_from_url_auto = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.xinyi_63000020,
            fullname="國家鐵道博物館",
            code_name="Nrm",
            external_link="https://www.nrm.gov.tw/News_actives.aspx?n=3325&sms=13412",
            branch_coordinates=Coordinate(raw_coordinates="25.04759981549798, 121.56476041209898"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.nrm.gov.tw/News_actives.aspx?n=3325&sms=13412")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.find_all("a", {"class": "div-activity"})

    async def _get_item_data(self, client: httpx.AsyncClient, item: ExhibitionItem):
        has_address_cache = await self.cache.aget(f"{item.UUID}-address")
        if has_address_cache:
            item.address = has_address_cache
            return
        response = await client.get(item.source_url)
        soup = self.translation().translation_to_object(response.text)
        exhibition_location = None
        a_elements = soup.select("div.programicon_05 a")[1:]
        if a_elements:
            exhibition_location = ", ".join([a_element.get_text(strip=True) for a_element in a_elements])
        await self.cache.aset(f"{item.UUID}-address", exhibition_location, month_3())
        item.address = exhibition_location

    async def suffix_item_from_url_auto(self, items: list[ExhibitionItem]):
        asyncio_limit = get_asyncio_rate_limit(3, 30)
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client, asyncio_limit:
            tasks = [self._get_item_data(client, item) for item in items]
            await asyncio.gather(*tasks)


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImage

    await NrmRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
