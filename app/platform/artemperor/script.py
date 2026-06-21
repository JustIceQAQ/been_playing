import asyncio
import itertools
from enum import Enum
from typing import cast

import bs4
import httpx

from app.platform.artemperor.parse import ArtEmperorParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_cookies, generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import get_date, month_3


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
        all_response = []
        response = await client.get(
            "https://artemperor.tw/tidbits",
            *args,
            **kwargs,
            params={"content": ex_status.value, "page": 1, "region": 0, "year": get_date.now_year},
        )
        response.raise_for_status()
        response_text = response.text

        all_response.append(response_text)

        response_object = BeautifulSoupTranslation().translation_to_object(response_text)
        if response_object is None:
            return None

        page_size = response_object.select_one("input#PG_size")
        if page_size is None:
            end_page = 10
        else:
            end_page = int(page_size.attrs.get("value", 10))
        tasks = [
            client.get(
                "https://artemperor.tw/tidbits",
                *args,
                **kwargs,
                params={"content": ex_status.value, "page": page, "region": 0, "year": get_date.now_year},
            )
            for page in range(2, end_page + 1)
        ]
        responses = await asyncio.gather(*tasks)
        all_response.extend([response.text for response in responses])
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

    def _check_list_box(self, datas: bs4.ResultSet[bs4.Tag]) -> bool:
        return (len(datas) != 1) and (datas[0].find("a").attrs.get("href") != "https://artemperor.tw//")

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        items = []
        for p in parsed:
            list_box = p.select("div.list_box")
            if self._check_list_box(list_box):
                items.extend(list_box)
        return items


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await ArtEmperorRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
