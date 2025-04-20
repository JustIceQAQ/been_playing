import asyncio

import bs4

from app.exhibition.jam.parse import JamParse
from helpers.cache.disk import DiskCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class JamRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = JamParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="忠泰美術館",
            code_name="Jam",
            external_link="https://jam.jutfoundation.org.tw/online-exhibition",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "Host": "jam.jutfoundation.org.tw",
            "Referer": "http://jam.jutfoundation.org.tw",
        }

        async with HttpxAsyncClient() as client:
            urls = [
                "https://jam.jutfoundation.org.tw/online-exhibition",
                "https://jam.jutfoundation.org.tw/coming-exhibition",
            ]
            tasks = [
                client.get(
                    url,
                    headers=headers,
                )
                for url in urls
            ]
            responses = await asyncio.gather(*tasks)
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parseds: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        data = []
        for parsed in parseds:
            data.extend(parsed.select("div.view-content > div.views-row"))
        return data


async def main():
    await JamRunner().run(DiskCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
