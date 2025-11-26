import asyncio

import bs4
from app.exhibition.tnammuseum.parse import TnamMuseumParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class TnamMuseumRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TnamMuseumParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="臺南市美術館",
            code_name="TnamMuseum",
            external_link="https://www.tnam.museum/exhibition/current?page=1"
        )

    async def fetch_response(self):
        headers = dict(**get_header())
        responses = []
        async with HttpxAsyncClient(headers=headers) as client:
            for url in ["https://www.tnam.museum/exhibition/current", "https://www.tnam.museum/exhibition/upcoming"]:
                page = 1
                while True:
                    sub_response = await client.get(url,
                                                    params={"page": page})
                    sub_soup = bs4.BeautifulSoup(sub_response.text, "html.parser")
                    has_items = sub_soup.select("div.layout-large > figure > a")
                    if has_items:
                        responses.append(sub_response.text)
                        page += 1
                        continue
                    break

        return responses

    async def fetch_parsed(self):
        parseds: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        dataset = []
        for parsed in parseds:
            dataset.extend(parsed.select("div.layout-large > figure > a"))

        return dataset


async def main():
    await TnamMuseumRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
