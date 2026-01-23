import asyncio

import bs4

from app.galleries.xizhitang.parse import XiZhiTangParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class XiZhiTangRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = XiZhiTangParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="羲之堂畫廊",
            code_name="XiZhiTang",
            external_link="https://taipeiartweek.tw/",
            branch_coordinates=Coordinate(raw_coordinates="25.040329571305197, 121.56247655631785"),
            venue_type=VenueType.GALLERY,
        )

    async def fetch_response(self):
        headers = generate_headers(host="www.xizhitang.com.tw")
        cookies = generate_cookies(need_phpsessid=True)
        async with HttpxAsyncClient(headers=headers, cookies=cookies) as client:
            response = await client.get("https://www.xizhitang.com.tw/tidbits")
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div.item-news")


async def main():
    await XiZhiTangRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
