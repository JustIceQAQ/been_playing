import asyncio

import bs4

from app.galleries.yiyun.parse import YiYunParse
from helpers.headers_helper import get_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class YiYunRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = YiYunParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="異雲書屋",
            code_name="YiYun",
            external_link="https://www.yiyun-art.com/",
            branch_coordinates=[
                Coordinate(location_code=TaiwanCity.taipei_city, name="青田館",
                           raw_coordinates="25.027213880907816, 121.53055350558525"),
                Coordinate(location_code=TaiwanCity.taipei_city, name="金華館",
                           raw_coordinates="25.028205131565272, 121.53223852023619"),
            ],
        )

    async def fetch_response(self):
        headers = get_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.yiyun-art.com/exhibitions")
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        current = parsed.find("div", {"id": "current"})
        following = parsed.find("div", {"id": "following"})
        followings = following.find_all("a", {"class": "exhibition-list"})
        followings.append(current)
        return followings


async def main():
    await YiYunRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
