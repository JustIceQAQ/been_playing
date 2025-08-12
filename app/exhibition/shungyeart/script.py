import asyncio
import uuid

import bs4
from app.exhibition.shungyeart.parse import ShungYeArtParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class ShungYeArtRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = ShungYeArtParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="順益台灣美術館",
            code_name="ShungYeArt",
            external_link="https://www.shungye-art.org/show_now.php",
        )

    async def fetch_response(self):
        url = "https://www.shungye-art.org/show_now.php"
        headers = {**get_header(), "referer": url}
        cookies = {
            "CONSENT": "YES+",
            "PHPSESSID": uuid.uuid4().hex,
        }

        async with HttpxAsyncClient(headers=headers, cookies=cookies) as client:
            response = await client.get(url)
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        now = parsed.find("a", {"id": "Now"}).find_all_next(class_="indexnews1")
        notice = parsed.find("a", {"id": "Notice"}).find_all_next(class_="indexnews1")
        now_ex = now + notice
        return now_ex


async def main():
    await ShungYeArtRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
