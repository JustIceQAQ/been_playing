import asyncio
import itertools
from enum import Enum

import bs4
import httpx

from app.platform.artemperor.parse import ArtEmperorParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.storage.symbol import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class ExStatus(int, Enum):
    current = 1
    upcoming = 2


class ArtEmperorRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = ArtEmperorParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="非池中藝術網",
            code_name="ArtEmperor",
            external_link="https://artemperor.tw/",
            venue_type=VenueType.PLATFORM,
        )

    async def fetch_process(self, client: httpx.AsyncClient, ex_status: ExStatus):
        all_response = []

        response = await client.get(
            "https://artemperor.tw/tidbits",
            params={"sort": ex_status.value, "page": 1}
        )
        response.raise_for_status()
        response_text = response.text
        all_response.append(response_text)

        p = BeautifulSoupTranslation().translation_to_object(response_text)
        end_page = int(p.find("input", {"id": "PG_size"}).get("value"))

        tasks = [
            client.get(
                "https://artemperor.tw/tidbits",
                params={"sort": ex_status.value, "page": page}
            )
            for page in range(2, end_page + 1)
        ]
        tasks_response = await asyncio.gather(*tasks)
        all_response.extend([task.text for task in tasks_response])

        return all_response

    async def fetch_response(self):
        headers = generate_headers(need_upgrade_insecure_requests=True)
        cookies = generate_cookies(need_phpsessid=True)
        async with asyncio.Semaphore(10):
            async with HttpxAsyncClient(headers=headers, cookies=cookies) as client:
                tasks = await asyncio.gather(
                    self.fetch_process(client, ExStatus.current),
                    self.fetch_process(client, ExStatus.upcoming)

                )
        flattened = list(itertools.chain.from_iterable(tasks))
        return flattened

    async def fetch_parsed(self):
        parsed: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        items = []
        for p in parsed:
            items.extend(p.select("div.list_box"))

        return items


async def main():
    await ArtEmperorRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
