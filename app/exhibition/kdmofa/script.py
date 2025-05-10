import asyncio
import secrets

import bs4
from app.exhibition.kdmofa.parse import KdMoFaParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class KdMoFaRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KdMoFaParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="關渡美術館",
            code_name="KdMoFa",
            external_link="https://kdmofa.tnua.edu.tw/mod/exhibition/index.php",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "host": "kdmofa.tnua.edu.tw",
            "referer": "https://kdmofa.tnua.edu.tw",
            "upgrade-insecure-requests": "1",
        }
        cookies = {"PHPSESSID": secrets.token_hex(13)}
        async with HttpxAsyncClient(headers=headers, cookies=cookies) as client:
            response = await client.get(
                "https://kdmofa.tnua.edu.tw/mod/exhibition/index.php"
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div.items > a.item")


async def main():
    await KdMoFaRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
