import asyncio

import bs4
from app.exhibition.tncsec.parse import TnCsEcParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class TnCsEcRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TnCsEcParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="國立臺南生活美學館",
            code_name="tncsec",
            external_link="https://www.tncsec.gov.tw/News_actives.aspx?n=2921&sms=11885&page=1&PageSize=30"
        )

    async def fetch_response(self):
        headers = dict(**get_header())
        url = "https://www.tncsec.gov.tw/News_actives.aspx?n=2921&sms=11885&page=1&PageSize=30"
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(url)
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        items = parsed.find("div", {"class": "group-list message"})
        if items is None:
            return None
        return items.find_all("a", {"class": "div-activity"})


async def main():
    await TnCsEcRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
