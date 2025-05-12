import asyncio

import bs4
import httpx

from app.exhibition.ntpc.parse import NTPCParse, normalize_date_range
from helpers.cache import DiskCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import ExhibitionItem, Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3, get_asyncio_rate_limit


class NTPCRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NTPCParse
    use_suffix_item_from_url_auto = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="NTPC",
            code_name="NTPC",
            external_link="https://www.ceramics.ntpc.gov.tw/xmdoc?xsmsid=0J148497613881029302",
        )

    def get_this_header(self):
        return {
            **get_header(),
            "upgrade-insecure-requests": "1",
            "host": "www.ceramics.ntpc.gov.tw",
        }

    async def fetch_response(self):
        headers = self.get_this_header()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://www.ceramics.ntpc.gov.tw/xmdoc?xsmsid=0J148497613881029302"
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div.ListPicText > div.item")

    async def suffix_data(self, client: httpx.AsyncClient, item: ExhibitionItem):
        has_date_cache = await self.cache.get(f"{item.UUID}-date")
        has_address_cache = await self.cache.get(f"{item.UUID}-address")
        if has_date_cache and has_address_cache:
            item.date = has_date_cache
            item.address = has_address_cache
            return

        response = await client.get(item.source_url)
        soup = self.translation().translation_to_object(response.text)
        exhibition_time = None
        exhibition_location = None
        p_tags = soup.select("div.district p")
        for p in p_tags:
            text = p.get_text(strip=True)
            if text.startswith("展覽時間："):
                exhibition_time = normalize_date_range(
                    text.replace("展覽時間：", "").strip()
                )
            elif text.startswith("展覽地點："):
                exhibition_location = text.replace("展覽地點：", "").strip()

        await self.cache.set(f"{item.UUID}-date", exhibition_time, month_3())
        await self.cache.set(f"{item.UUID}-address", exhibition_location, month_3())

        item.date = exhibition_time
        item.address = exhibition_location

    async def suffix_item_from_url_auto(self, items: list[ExhibitionItem]):
        headers = self.get_this_header()
        asyncio_limit = get_asyncio_rate_limit(3, 30)
        async with HttpxAsyncClient(headers=headers) as client, asyncio_limit:
            await asyncio.gather(*[self.suffix_data(client, item) for item in items])


async def main():
    await NTPCRunner().run(DiskCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
