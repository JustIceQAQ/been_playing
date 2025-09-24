import asyncio

import bs4
from app.platform.cultureexpress.parse import CultureExpressParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class CultureExpressRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = CultureExpressParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="文化快遞",
            code_name="CultureExpress",
            external_link="https://cultureexpress.taipei/Event/C000003",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "referer": "https://cultureexpress.taipei",
        }
        responses = []
        async with HttpxAsyncClient(headers=headers) as client:
            init_response = await client.get(
                url="https://cultureexpress.taipei/Event/C000003"
            )
            init_response.raise_for_status()
            page_index = 1
            while True:
                response = await client.get(
                    "https://cultureexpress.taipei/Event/C000003",
                    params={
                        "CategoryID": "b89f200f-61e0-4956-9c2e-c90d5285ac67",
                        "DateRange": 0,
                        "PageIndex": page_index,
                    },
                )
                if response.is_success:
                    responses.append(response)
                    page_index += 1
                else:
                    break
        return responses

    async def fetch_parsed(self):
        dataset = []
        parseds: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        for parsed in parseds:
            dataset.extend(parsed.select("div#block  div.card"))
        return dataset


async def main():
    await CultureExpressRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
