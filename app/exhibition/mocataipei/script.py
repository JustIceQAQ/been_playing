import asyncio

import bs4

from app.exhibition.mocataipei.parse import MoCaTaipeiParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class MoCaTaipeiRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = MoCaTaipeiParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="台北當代藝術館",
            code_name="MoCaTaipei",
            external_link="https://www.mocataipei.org.tw/tw/ExhibitionAndEvent",
            address="台北市大同區103長安西路39號 ",
            google_map_place_id="ChIJc-TxSWypQjQR-8Eh7elK97Q",
        )

    async def fetch_response(self):
        headers = get_header()
        target_url = [
            "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent",
            "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent/Exhibitions/Upcoming",
        ]
        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [client.get(url) for url in target_url]
            tasks_response = await asyncio.gather(*tasks)
        return [task.text for task in tasks_response]

    async def fetch_parsed(self):
        parsers: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        items_dataset = []
        for parsed in parsers:
            if runtime_element := parsed.select("div.listFrameBox div.list"):
                items_dataset.extend(runtime_element)
        return items_dataset

    async def fetch_items(self, *args, **kwargs):
        return await super().fetch_items(target_domain="https://www.mocataipei.org.tw")


async def main():
    await MoCaTaipeiRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
