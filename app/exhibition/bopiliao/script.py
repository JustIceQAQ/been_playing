import asyncio

import httpx

from app.exhibition.bopiliao.parse import BoPiLiaoParse
from helpers.cache.none.helper import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class BoPiLiaoRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = BoPiLiaoParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="剝皮寮歷史街區",
            code_name="BoPiLiao",
            external_link="https://www.bopiliao.taipei/Event_News",
        )

    async def _fetch_url(
        self, client: httpx.AsyncClient, url: str, params: dict
    ) -> httpx.Response:
        return await client.get(url, params=params)

    async def fetch_response(self):
        headers = {**get_header(), "host": "www.bopiliao.taipei"}
        params = {
            "ajax": 1,
            "search_day_start": "",
            "search_day_end": "",
            "pageSize": 10,
            "pageNumber": 1,
        }
        urls = (
            "https://www.bopiliao.taipei/Event_News/new",
            "https://www.bopiliao.taipei/Event_News/now",
        )

        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [self._fetch_url(client, url, params) for url in urls]
            tasks_response = await asyncio.gather(*tasks)
        return tasks_response

    async def fetch_parsed(self):
        items = []
        parsed: list[httpx.Response] = await super().fetch_parsed()
        for item in parsed:
            items.extend(item.json()["items"])
        return items


async def main():
    await BoPiLiaoRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
