import asyncio

import bs4

from app.exhibition.mocataipei.parse import MoCaTaipeiParse
from helpers.cache.none import NoneCache
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
            map_url=(
                "https://www.google.com/maps/embed?"
                "pb=!1m18!1m12!1m3!1d3614.5072784351205!2d121.51563993159156!"
                "3d25.05079012059311!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!"
                "3m3!1m2!1s0x3442a96c49f1e473%3A0xb4f74ae9ed21c1fb!2z5Y-"
                "w5YyX55W25Luj6Jed6KGT6aSo!5e0!3m2!1szh-TW!2stw!4v1739201393858!5m2!1szh-TW!2stw"
            ),
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
