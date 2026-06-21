import asyncio

import bs4

from app.platform.udnfunlife.parse import UdnFunLifeParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from typing import cast


class UdnFunLifeRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = UdnFunLifeParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="udn售票網",
            code_name="UdnFunLife",
            external_link="https://tickets.udnfunlife.com/application/UTK01/UTK0101_03.aspx?Category=231&kdid=cateList",
            venue_type=VenueType.PLATFORM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post(
                "https://tickets.udnfunlife.com/Application/UTK01/UTK0101_009.aspx/Product_Category_List",
                json={"category": "231", "pageNo": "1", "pageSize": "50"},
            )
        return response.json()["d"]["ReturnData"]["script"]

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("div.inner")


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await UdnFunLifeRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
