import asyncio

import bs4
import httpx

from app.exhibition.songshanculturalpark.parse import SongShanCulturalParkParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, ExhibitionItem
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3, get_asyncio_rate_limit


class SongShanCulturalParkRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = SongShanCulturalParkParse
    use_suffix_item_from_url_auto = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="松山文創園區",
            code_name="SongShanCulturalPark",
            external_link="https://www.songshanculturalpark.org/exhibition",
        )

    async def fetch_response(self):
        headers = get_header()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://www.songshanculturalpark.org/exhibition"
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div#exhibition > div.rows")

    async def fetch_items(self, *args, **kwargs):
        items = await super().fetch_items(
            target_domain="https://www.songshanculturalpark.org"
        )
        return items

    async def _get_item_data(self, client: httpx.AsyncClient, item: ExhibitionItem):
        has_address_cache = await self.cache.get(f"{item.UUID}-address")
        if has_address_cache:
            item.address = has_address_cache
            return
        response = await client.get(item.source_url)
        soup = self.translation().translation_to_object(response.text)
        exhibition_location = None
        p_tags = soup.find("p", {"class": "place"})
        if p_tags:
            exhibition_location = p_tags.get_text()
        await self.cache.set(f"{item.UUID}-address", exhibition_location, month_3())
        item.address = exhibition_location

    async def suffix_item_from_url_auto(self, items: list[ExhibitionItem]):
        asyncio_limit = get_asyncio_rate_limit(3, 30)
        headers = get_header()
        async with httpx.AsyncClient(headers=headers) as client, asyncio_limit:
            tasks = [self._get_item_data(client, item) for item in items]
            await asyncio.gather(*tasks)


async def main():
    await SongShanCulturalParkRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
