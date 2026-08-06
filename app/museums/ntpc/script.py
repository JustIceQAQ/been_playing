import asyncio
from typing import cast

import bs4

from app.museums.ntpc.information import NTPCInformation
from app.museums.ntpc.parse import NTPCParse
from app.museums.ntpc.social_media import NTPCSocialMedia
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import ExhibitionItem, Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import get_asyncio_rate_limit, month_3


class NTPCRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NTPCParse
    use_suffix_item_from_url_auto = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return NTPCInformation.get_information()

    def set_social_media(self):
        return NTPCSocialMedia.get_social_media()

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

    async def suffix_data(self, client, item: ExhibitionItem):
        has_address_cache = await self.cache.aget(f"{item.UUID}-address")
        if has_address_cache:
            item.address = has_address_cache
            return

        response = await client.get(item.source_url)
        soup = self.translation().translation_to_object(response.text)
        if soup is None:
            return None
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
    from helpers.cache import none_cache
    from helpers.image_hosting import none_image_hosting

    await NTPCRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
