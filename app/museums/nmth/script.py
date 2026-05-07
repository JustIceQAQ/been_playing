import asyncio

import bs4

from app.museums.nmth.parse import NMTHParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage

from typing import cast


class NMTHRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NMTHParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.tainan.an_nan_67000350,
            fullname="國立臺灣歷史博物館",
            code_name="NMTH",
            external_link="https://www.nmth.gov.tw/",
            branch_coordinates=Coordinate(raw_coordinates="23.058163348092073, 120.23516300543494"),
            venue_type=VenueType.MEMORIAL,
        )

    async def fetch_response(self):
        headers = generate_headers()
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.nmth.gov.tw/News2.aspx?n=4105&sms=13791", cookies=cookies)
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("div.group-list li div.area-essay")


async def main():
    await NMTHRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
