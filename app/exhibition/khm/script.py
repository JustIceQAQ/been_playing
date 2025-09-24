import asyncio

import bs4
import httpx

from app.exhibition.khm.parse import KhmParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class KhmRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KhmParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="高雄市立歷史博物館",
            code_name="khm",
            external_link="https://khm.org.tw/tw",
        )

    async def sub_get_response(self, client: httpx.AsyncClient, url: str) -> str:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

    async def fetch_response(self):
        current_exhibitions_url = "https://khm.org.tw/tw/exhibition/currentexhibitions"
        permanent_exhibitions = "https://khm.org.tw/tw/exhibition/permanentexhibitions"
        headers = {**get_header(), "referer": current_exhibitions_url}
        async with httpx.AsyncClient(headers=headers) as client:
            current_exhibitions_response = await self.sub_get_response(
                client, current_exhibitions_url
            )
            permanent_exhibitions = await self.sub_get_response(
                client, permanent_exhibitions
            )
        return [current_exhibitions_response, permanent_exhibitions]

    async def fetch_parsed(self):
        dataset = []
        parsed: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        for soup in parsed:
            datas = soup.select("div.exhibition-list div.list-item")
            dataset.extend(datas)
        return dataset


async def main():
    await KhmRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
