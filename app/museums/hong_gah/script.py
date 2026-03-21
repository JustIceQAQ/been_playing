import asyncio

import bs4
from rnet.rnet import Proxy

from app.museums.hong_gah.parse import HongGahParse
from configs.settings import get_settings
from helpers.crawler.rnet.helper import RNetAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class HongGahRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = HongGahParse
    is_sort: bool = False
    is_unique: bool = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="鳳甲美術館",
            code_name="HongGah",
            external_link="https://hong-gah.org.tw/exhibitions-zh",
            branch_coordinates=Coordinate(
                raw_coordinates="25.125315737958747, 121.49922632559256"
            ),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            host="hong-gah.org.tw",
            referer="https://hong-gah.org.tw/exhibitions-zh",
            x_requested_with="XMLHttpRequest",
        )
        runtime_settings = get_settings()
        proxies = (
            None
            if runtime_settings.PROXY_POOL is None
            else [Proxy.all(runtime_settings.PROXY_POOL)]
        )
        async with RNetAsyncClient(
            headers=headers,
            follow_redirects=True,
            proxies=proxies,
        ) as client:
            response = await client.get("https://hong-gah.org.tw/exhibitions-zh")
        return await response.text()

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        project = parsed.find("div", {"class": "portfolio-grid"})
        items = project.find_all("div", {"class": "ohio-project-item"})
        return items


async def main():
    await HongGahRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
