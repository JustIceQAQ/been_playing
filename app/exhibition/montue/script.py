import asyncio

import bs4
import httpx

from app.exhibition.montue.parse import MoNTUEParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class MoNTUERunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = MoNTUEParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="北師美術館",
            code_name="MoNTUE",
            external_link="https://montue.ntue.edu.tw/"
        )

    async def sub_fetch_response(self, client: httpx.AsyncClient, url: str) -> str:
        response = await client.get(url)
        return response.text

    async def fetch_response(self):
        headers = dict(**get_header())
        urls = [
            "https://montue.ntue.edu.tw/exhibitions/",
            "https://montue.ntue.edu.tw/exhibitions-upcoming/",
        ]
        async with HttpxAsyncClient(headers=headers) as client:
            get_a_tasks = [
                self.sub_fetch_response(client, url)
                for url in urls
            ]
            all_items_url = []
            get_a_results = await asyncio.gather(*get_a_tasks)
            for result in get_a_results:
                soup = BeautifulSoupTranslation().translation_to_object(result)
                divs = soup.find_all("div", {"class": "ptsc pt-sc sc-slider exhibition-slider hide-title hide-mobile"})
                for div in divs:
                    all_items_url.append(div.find("a").get("href"))
            get_items_context = [
                self.sub_fetch_response(client, item_url)
                for item_url in all_items_url
            ]
            get_items_context_results = await asyncio.gather(*get_items_context)
        return get_items_context_results

    async def fetch_parsed(self):
        parsed: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        return parsed


async def main():
    await MoNTUERunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
