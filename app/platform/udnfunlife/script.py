import asyncio

import bs4

from app.platform.udnfunlife.parse import UdnFunLifeParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


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
        )

    async def fetch_response(self):
        headers = get_header()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post(
                "https://tickets.udnfunlife.com/Application/UTK01/UTK0101_009.aspx/Product_Category_List",
                json={"category": "231", "pageNo": "1", "pageSize": "50"},
            )
        return response.json()["d"]["ReturnData"]["script"]

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div.inner")


async def main():
    await UdnFunLifeRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
