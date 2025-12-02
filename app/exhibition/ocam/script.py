import asyncio
import secrets

import bs4

from app.exhibition.ocam.parse import OCAMParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class OCAMRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = OCAMParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="陽明海洋文化藝術館",
            code_name="OCAM",
            external_link="https://www.ymculture.org.tw/tw/Exhibition/OCAM#",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "referer": "https://www.ymculture.org.tw/tw/Exhibition/OCAM#",
        }
        cookies = {"PHPSESSID": secrets.token_hex(16)}
        url = "https://www.ymculture.org.tw/tw/Exhibition/OCAM#"
        async with HttpxAsyncClient(headers=headers, cookies=cookies) as client:
            response = await client.get(url)
            response.raise_for_status()
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("ul#eachList li")


async def main():
    await OCAMRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
