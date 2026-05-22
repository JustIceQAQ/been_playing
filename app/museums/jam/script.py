import asyncio
from typing import cast

import bs4

from app.museums.jam.parse import JamParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class JamRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = JamParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.daan_63000030,
            fullname="忠泰美術館",
            code_name="Jam",
            external_link="https://jam.jutfoundation.org.tw/online-exhibition",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.044509020251724, 121.53731469675466"),
                raw_coordinates="25.044509020251724, 121.53731469675466",
            ),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="jam.jutfoundation.org.tw", referer="https://jam.jutfoundation.org.tw")

        async with HttpxAsyncClient(headers=headers) as client:
            urls = [
                "https://jam.jutfoundation.org.tw/online-exhibition",
                "https://jam.jutfoundation.org.tw/coming-exhibition",
            ]
            tasks = [
                client.get(
                    url,
                )
                for url in urls
            ]
            responses = await asyncio.gather(*tasks)
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parseds = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        data = []
        for parsed in parseds:
            data.extend(parsed.select("div.view-content > div.views-row"))
        return data


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await JamRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
