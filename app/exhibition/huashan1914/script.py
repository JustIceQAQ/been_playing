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
            map_url=(
                "https://www.google.com/maps/embed?pb="
                "!1m18!1m12!1m3!1d3614.70526064475!2d121.52678337571571!"
                "3d25.044074637885124!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!"
                "4f13.1!3m3!1m2!1s0x3442a96523e0246d%3A0xf1c9276707165c71!"
                "2z6I-v5bGxMTkxNOaWh-WMluWJteaEj-eUoualreWckuWNgA!5e0!3m2!"
                "1szh-TW!2stw!4v1739201056327!5m2!1szh-TW!2stw"
            ),
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
