import asyncio
from typing import cast

import bs4

from app.museums.mwr.parse import MwrParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class MwrRunner(RunnerInit):
    """世界宗教博物館"""

    translation = BeautifulSoupTranslation
    use_parse = MwrParse
    use_suffix_item_from_file_func = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.new_taipei.yonghe_65000040,
            fullname="世界宗教博物館",
            code_name="Mwr",
            external_link="https://www.mwr.org.tw/xcpmtexhi?xsmsid=0H305740978429024070",
            branch_coordinates=Coordinate(raw_coordinates="25.008202799610107, 121.50783679675385"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        xsmsid = "0H305741810776620070"
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(f"https://www.mwr.org.tw/xcspecexhi?xsmsid={xsmsid}")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("div.ce_list > div.item")


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await MwrRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
