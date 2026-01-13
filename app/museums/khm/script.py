import asyncio

import bs4
from rnet import Proxy, Client
from app.museums.khm.parse import KhmParse
from configs.settings import get_settings
from helpers.crawler.rnet.helper import RNetAsyncClient
from helpers.headers_helper import get_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity
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
            location_code=TaiwanCity.kaohsiung_city,
            fullname="高雄市立歷史博物館",
            code_name="khm",
            external_link="https://khm.org.tw/tw",
            branch_coordinates=Coordinate(raw_coordinates="22.62712833389164, 120.28687449855717"),
        )

    async def sub_get_response(self, client: Client, url: str) -> str:
        response = await client.get(url)
        return await response.text()

    async def fetch_response(self):
        current_exhibitions_url = "https://khm.org.tw/tw/exhibition/currentexhibitions"
        permanent_exhibitions = "https://khm.org.tw/tw/exhibition/permanentexhibitions"
        headers = get_headers(referer=current_exhibitions_url, not_use_user_agent=True)
        runtime_settings = get_settings()
        proxies = (
            None
            if runtime_settings.PROXY_POOL is None
            else [
                Proxy.all(
                    runtime_settings.PROXY_POOL
                )
            ]
        )
        async with RNetAsyncClient(
                proxies=proxies, headers=headers,
        ) as client:
            responses = await asyncio.gather(
                self.sub_get_response(
                    client, current_exhibitions_url
                ),
                self.sub_get_response(
                    client, permanent_exhibitions
                )
            )
        return responses

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
