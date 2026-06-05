import asyncio
from typing import cast

import bs4
from app.museums.n228mm.parse import N228MMParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class N228MMRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = N228MMParse
    is_sort = False
    is_unique = False
    use_suffix_item_from_file_func = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.zhongzheng_63000050,
            fullname="二二八國家紀念館",
            code_name="n228mm",
            external_link="https://www.228.org.tw/exhibitionsnew",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.03187889577739, 121.51386505257408"),
                raw_coordinates="25.03187889577739, 121.51386505257408",
            ),
            venue_type=VenueType.MEMORIAL,
        )

    async def fetch_response(self):
        headers = generate_headers(other_headers={"accept-encoding": "gzip, deflate, zstd"})
        async with HttpxAsyncClient(headers=headers) as client:
            response_1 = await client.get(
                "https://www.228.org.tw/exhibitionsnew",
            )
        return response_1.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("div[role='listitem']")


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await N228MMRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
