import asyncio
from typing import cast

import bs4

from app.museums.chiayimm.parse import ChiayiMMParse
from helpers.crawler.headers_helper import generate_cookies, generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class ChiayiMMRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = ChiayiMMParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.chiayi_city.east_10020010,
            fullname="嘉義市立博物館",
            code_name="ChiayiMM",
            external_link="https://museum.chiayi.gov.tw/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="23.487196187060913, 120.45171887377413"),
                raw_coordinates="23.487196187060913, 120.45171887377413",
            ),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            referer="https://museum.chiayi.gov.tw/",
            host="museum.chiayi.gov.tw",
        )
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with HttpxAsyncClient(headers=headers, use_proxy=True) as client:
            urls = [
                "https://museum.chiayi.gov.tw/ExhibitionListC003310.aspx?appname=ExhibitionListC003310&SearchAdvanced=true",
                "https://museum.chiayi.gov.tw/ExhibitionListC003310.aspx?appname=ExhibitionListC003320&SearchAdvanced=true",
            ]
            responses = await asyncio.gather(*[client.get(url, cookies=cookies) for url in urls])
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        items = []
        for p in parsed:
            items.extend(p.select("div.kf-diagramtext-col a.kf-item"))
        return items


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await ChiayiMMRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
