import asyncio

import bs4

from app.museums.ocam.parse import OCAMParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3

from typing import cast


class OCAMRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = OCAMParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.keelung.renai_10017040,
            fullname="陽明海洋文化藝術館",
            code_name="OCAM",
            external_link="https://www.ymculture.org.tw/tw/Exhibition/OCAM#",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.132752348069353, 121.7400201544287"),
                raw_coordinates="25.132752348069353, 121.7400201544287",
            ),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(referer="https://www.ymculture.org.tw/tw/Exhibition/OCAM#")
        cookies = generate_cookies(need_phpsessid=True)
        url = "https://www.ymculture.org.tw/tw/Exhibition/OCAM#"
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(url, cookies=cookies)
            response.raise_for_status()
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("ul#eachList li")


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await OCAMRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
