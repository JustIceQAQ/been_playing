import asyncio

import bs4

from app.exhibition.songshanculturalpark.parse import SongShanCulturalParkParse
from helpers.cache.none.helper import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class SongShanCulturalParkRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = SongShanCulturalParkParse

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


async def main():
    await SongShanCulturalParkRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
