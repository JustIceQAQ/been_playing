import asyncio

import bs4

from app.galleries.ruomu.parse import RuoMuParse
from helpers.headers_helper import get_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class RuoMuRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = RuoMuParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="若木藝廊",
            code_name="RuoMu",
            external_link="https://www.ruomugallery.com/",
            branch_coordinates=Coordinate(raw_coordinates="25.033909532791032, 121.52358387976376"),
        )

    async def fetch_response(self):
        headers = get_headers(
            need_upgrade_insecure_requests=True,
            host="www.ruomugallery.com",
        )
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.ruomugallery.com/exhibitions/")
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("#exhibitions-grid-current li")



async def main():
    await RuoMuRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())