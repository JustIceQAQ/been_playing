import asyncio

import bs4
import httpx

from app.museums.ntpc.parse import NTPCParse
from helpers.cache import DiskCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.image_hosting.none.helper import NoneImageHosting
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import ExhibitionItem, Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3, get_asyncio_rate_limit

from typing import cast


class NTPCRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NTPCParse
    use_suffix_item_from_url_auto = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.new_taipei.yingge_65000080,
            fullname="新北市立鶯歌陶瓷博物館",
            code_name="NTPC",
            external_link="https://www.ceramics.ntpc.gov.tw/xmdoc?xsmsid=0J148497613881029302",
            branch_coordinates=Coordinate(raw_coordinates="24.949406697655782, 121.3520648774411"),
            venue_type=VenueType.MUSEUM,
        )

    def get_this_header(self):
        return generate_headers(host="www.ceramics.ntpc.gov.tw", need_upgrade_insecure_requests=True)

    async def fetch_response(self):
        headers = self.get_this_header()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.ceramics.ntpc.gov.tw/xmdoc?xsmsid=0J148497613881029302")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("div.ListPicText > div.item")

    async def suffix_data(self, client: httpx.AsyncClient, item: ExhibitionItem):
        has_address_cache = await self.cache.aget(f"{item.UUID}-address")
        if has_address_cache:
            item.address = has_address_cache
            return

        response = await client.get(item.source_url)
        soup = self.translation().translation_to_object(response.text)
        exhibition_location = None
        for selector in ("div.district p", "div.district h3"):
            for tag in soup.select(selector):
                text = tag.get_text(strip=True)
                if text.startswith("展覽地點"):
                    exhibition_location = text.replace("展覽地點", "").replace("：", "").replace("︱", "").strip()
                    break
            if exhibition_location:
                break
        await self.cache.aset(f"{item.UUID}-address", exhibition_location, month_3())

        item.address = exhibition_location

    async def suffix_item_from_url_auto(self, items: list[ExhibitionItem]):
        headers = self.get_this_header()
        asyncio_limit = get_asyncio_rate_limit(3, 30)
        async with HttpxAsyncClient(headers=headers) as client, asyncio_limit:
            await asyncio.gather(*[self.suffix_data(client, item) for item in items])


async def main():
    await NTPCRunner().run(DiskCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
