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
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage

from typing import cast


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

    async def fetch_process(self, client: httpx.AsyncClient, ex_status: ExStatus, *args, **kwargs):
        response = await client.get(
            "https://artemperor.tw/tidbits",
            *args,
            **kwargs,
            params={"sort": ex_status.value, "page": 1},
        )
        response.raise_for_status()
        response_text = response.text
        list_box_len = len(BeautifulSoupTranslation().translation_to_object(response_text).select("div.list_box"))
        all_response = []
        end_page = 1
        while list_box_len > 1:
            all_response.append(response_text)
            end_page += 1
            response = await client.get(
                "https://artemperor.tw/tidbits",
                *args,
                **kwargs,
                params={"sort": ex_status.value, "page": end_page},
            )
            list_box_len = len(BeautifulSoupTranslation().translation_to_object(response.text).select("div.list_box"))
            await asyncio.sleep(1)
        return all_response

    async def fetch_response(self):
        headers = generate_headers(need_upgrade_insecure_requests=True)
        cookies = generate_cookies(need_phpsessid=True)
        async with asyncio.Semaphore(10):
            async with HttpxAsyncClient(headers=headers) as client:
                tasks = await asyncio.gather(
                    self.fetch_process(client, ExStatus.current, cookies=cookies),
                    self.fetch_process(client, ExStatus.upcoming, cookies=cookies),
                )
        flattened = list(itertools.chain.from_iterable(tasks))
        return flattened

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        items = []
        for p in parsed:
            items.extend(p.select("div.list_box"))

        return items


async def main():
    await ArtEmperorRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
