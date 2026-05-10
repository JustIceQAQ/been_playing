import asyncio

import bs4
from typing import cast
from app.museums.chiayiam.parse import ChiayiAMParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class ChiayiAMRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = ChiayiAMParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.chiayi_city.west_10020020,
            fullname="嘉義市立美術館",
            code_name="ChiayiAM",
            external_link="https://chiayiartmuseum.chiayi.gov.tw/",
            branch_coordinates=Coordinate(raw_coordinates="23.476964512470964, 120.44092961904913"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            host="chiayiartmuseum.chiayi.gov.tw",
            referer="https://chiayiartmuseum.chiayi.gov.tw/ExhibitionsListC003100.aspx?appname=Exhibition3120",
        )
        async with HttpxAsyncClient(headers=headers) as client:
            urls = [
                "https://chiayiartmuseum.chiayi.gov.tw/ExhibitionsListC003100.aspx?appname=Exhibition3110",
                "https://chiayiartmuseum.chiayi.gov.tw/ExhibitionsListC003100.aspx?appname=Exhibition3120",
            ]
            responses = await asyncio.gather(*[client.get(url) for url in urls])
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        items = []
        for p in parsed:
            items.extend(p.select("div.kf-diagramtext-col a.kf-item"))
        return items


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await ChiayiAMRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
