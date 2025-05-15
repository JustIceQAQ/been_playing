import asyncio

import bs4

from app.exhibition.huashan1914.parse import huashan1914Parse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class HuaShan1914Runner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = huashan1914Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="華山1914文化創意產業園區",
            code_name="HuaShan1914",
            external_link="https://www.huashan1914.com/w/huashan1914/exhibition",
            address="台北市中正區八德路一段1號",
            google_map_place_id="ChIJbSTgI2WpQjQRcVwWB2cnyfE",
        )

    async def fetch_response(self):
        index = 1
        datasets = []
        async with HttpxAsyncClient() as client:
            while True:
                response = await client.get(
                    f"https://www.huashan1914.com/w/huashan1914/exhibition?index={index}",
                    headers=get_header(),
                )
                dataset = bs4.BeautifulSoup(response.text, "html5lib").select(
                    "ul#event-ul li"
                )
                if dataset:
                    datasets.append(response.text)
                    index = index + 1
                else:
                    break
        return datasets

    async def fetch_parsed(self):
        items = []
        parsers: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        for parsed in parsers:
            sub_items = parsed.select("ul#event-ul li")
            items.extend(sub_items)
        return items

    async def fetch_items(self, *args, **kwargs):
        return await super().fetch_items(target_domain="https://www.huashan1914.com")


async def main():
    await HuaShan1914Runner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
