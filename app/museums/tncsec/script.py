import asyncio
from typing import cast

import bs4

from app.museums.tncsec.parse import TnCsEcParse
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


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
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="22.992283833020835, 120.18735052369556"),
                raw_coordinates="22.992283833020835, 120.18735052369556",
            ),
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
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await TnCsEcRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
