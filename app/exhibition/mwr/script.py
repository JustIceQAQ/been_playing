import asyncio

import bs4

from app.exhibition.mwr.parse import MwrParse
from helpers.cache.none import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class MwrRunner(RunnerInit):
    """世界宗教博物館"""

    translation = BeautifulSoupTranslation
    use_parse = MwrParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="世界宗教博物館",
            code_name="Mwr",
            external_link="https://www.mwr.org.tw/xcpmtexhi?xsmsid=0H305740978429024070",
        )

    async def fetch_response(self):
        xsmsid = "0H305741810776620070"
        headers = get_header()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                f"https://www.mwr.org.tw/xcspecexhi?xsmsid={xsmsid}"
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div.ce_list > div.item")


async def main():
    await MwrRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
