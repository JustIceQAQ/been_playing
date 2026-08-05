import asyncio
from typing import cast

import bs4

from app.galleries.xizhitang.parse import XiZhiTangParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_cookies, generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class XiZhiTangRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = XiZhiTangParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.xinyi_63000020,
            fullname="羲之堂畫廊",
            code_name="XiZhiTang",
            external_link="https://taipeiartweek.tw/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.040329571305197, 121.56247655631785"),
                raw_coordinates="25.040329571305197, 121.56247655631785",
            ),
            venue_type=VenueType.GALLERY,
        )

    async def fetch_response(self):
        headers = generate_headers(host="www.xizhitang.com.tw")
        cookies = generate_cookies(need_phpsessid=True)
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.xizhitang.com.tw/tidbits", cookies=cookies)
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("div.item-news")


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await XiZhiTangRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
