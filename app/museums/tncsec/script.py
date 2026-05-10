import asyncio

import bs4
from app.museums.tncsec.parse import TnCsEcParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from typing import cast


class TnCsEcRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TnCsEcParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.tainan.west_central_67000370,
            fullname="國立臺南生活美學館",
            code_name="tncsec",
            external_link="https://www.tncsec.gov.tw/News_actives.aspx?n=2921&sms=11885&page=1&PageSize=30",
            branch_coordinates=Coordinate(raw_coordinates="22.992283833020835, 120.18735052369556"),
            venue_type=VenueType.EXPO_CENTER,
        )

    async def fetch_response(self):
        headers = generate_headers()
        url = "https://www.tncsec.gov.tw/News_actives.aspx?n=2921&sms=11885&page=1&PageSize=30"
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(url)
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        items = parsed.find("div", {"class": "group-list message"})
        if items is None:
            return None
        return items.find_all("a", {"class": "div-activity"})


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image.none.helper import NoneImage

    await TnCsEcRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
