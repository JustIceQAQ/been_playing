import asyncio

import bs4
from app.exhibition.chipolin.parse import ChiPoLinParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class ChiPoLinRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = ChiPoLinParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="齊柏林空間",
            code_name="ChiPoLin",
            external_link="https://www.chipolin.org/exhibition",
        )

    async def fetch_response(self):
        headers = dict(**get_header())
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.chipolin.org/exhibition")
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.find_all("li", {"class": "exhibition__item"})


async def main():
    await ChiPoLinRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
