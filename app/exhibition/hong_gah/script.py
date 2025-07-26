import asyncio

import bs4
from app.exhibition.hong_gah.parse import HongGahParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class HongGahRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = HongGahParse
    is_sort: bool = False
    is_unique: bool = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="鳳甲美術館",
            code_name="HongGah",
            external_link="https://hong-gah.org.tw/exhibitions-zh",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://hong-gah.org.tw/exhibitions-zh",
            "host": "hong-gah.org.tw",
        }
        async with HttpxAsyncClient(headers=headers, follow_redirects=True) as client:
            response = await client.get("https://hong-gah.org.tw/exhibitions-zh/page/1")
            response.raise_for_status()
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        project = parsed.find("div", {"class": "portfolio-grid"})
        items = project.find_all("div", {"class": "ohio-project-item"})
        return items


async def main():
    await HongGahRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
