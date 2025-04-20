import asyncio

import bs4

from app.exhibition.ntnu_art_museum.parse import NTNUArtMuseumParse
from helpers.cache.none import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NTNUArtMuseumRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NTNUArtMuseumParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="師大美術館",
            code_name="NTNUArtMuseum",
            external_link="https://www.artmuse.ntnu.edu.tw/index.php/current_exhibit/",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "host": "www.artmuse.ntnu.edu.tw",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://www.artmuse.ntnu.edu.tw/index.php/current_exhibit/"
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        items = parsed.select("figcaption")
        return [item.parent for item in items]


async def main():
    await NTNUArtMuseumRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
