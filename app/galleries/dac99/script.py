import asyncio

import bs4

from app.galleries.dac99.parse import Dac99Parse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class Dac99Runner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = Dac99Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="99度藝術中心",
            code_name="Dac99",
            external_link="https://99dac.com/exhibition.php",
            branch_coordinates=Coordinate(
                raw_coordinates="25.11649643071741, 121.5053916644182"
            ),
            venue_type=VenueType.GALLERY,
        )

    async def fetch_response(self):
        headers = generate_headers()
        cookies = generate_cookies(need_phpsessid=True)
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://99dac.com/exhibition.php", cookies=cookies
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div.exhibition-current div.exhibition-current__item")


async def main():
    await Dac99Runner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
