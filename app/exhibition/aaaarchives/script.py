import asyncio
import secrets

import bs4
from app.exhibition.aaaarchives.parse import AAAArchivesParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class AAAArchivesRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = AAAArchivesParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="國家發展委員會檔案管理局",
            code_name="AAAArchives",
            external_link="https://aaa.archives.tw/tw/event/306.html"
        )

    async def fetch_response(self):
        url = "https://aaa.archives.tw/tw/event/306.html"
        headers = {
            **get_header(),
            "referer": url,
            "origin": "https://aaa.archives.tw",
            "host": "aaa.archives.tw",
            "content-type": "application/x-www-form-urlencoded",
        }
        cookies = {
            "JSESSIONID": secrets.token_hex(16),
            "cookiesession1": secrets.token_hex(16)
        }
        data = {
            "nowPage": 1,
            "pageSize": 60,
        }
        async with HttpxAsyncClient(headers=headers, cookies=cookies, verify=False) as client:
            response = await client.post(url, data=data)
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        li = parsed.select("div.actList > ul > li")
        return li


async def main():
    await AAAArchivesRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
