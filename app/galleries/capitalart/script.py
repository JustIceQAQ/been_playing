import asyncio

import bs4

from app.galleries.capitalart.parse import CapitalArtParse
from helpers.headers_helper import get_headers, get_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class CapitalArtRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = CapitalArtParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="首都藝術中心",
            code_name="CapitalArt",
            external_link="https://capitalart.com.tw/",
            branch_coordinates=Coordinate(raw_coordinates="25.038294766316984, 121.55372725140036"),
        )

    async def fetch_response(self):
        headers = get_headers(need_upgrade_insecure_requests=True)
        cookies = get_cookies(need_laravel_session=True)

        urls = [
            "https://capitalart.com.tw/exhibitions.html",
            "https://capitalart.com.tw/exhibitions_upcoming.html"
        ]

        async with HttpxAsyncClient(headers=headers, cookies=cookies) as client:
            responses = await asyncio.gather(*[
                client.get(url)
                for url in urls
            ])
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parsed: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        datas = []
        for element in parsed:
            items = element.select("div.show-items")
            if items:
                datas.extend(items)

        return datas


async def main():
    await CapitalArtRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
