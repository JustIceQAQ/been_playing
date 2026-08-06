import asyncio
from typing import cast

import bs4

from app.museums.nhclac.parse import NhClAcParse
from helpers.crawler.headers_helper import generate_cookies, generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NhClAcRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NhClAcParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.hsinchu_city.east_10018010,
            fullname="國立新竹生活美學館",
            code_name="nhclac",
            external_link="https://www.nhclac.gov.tw/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="24.803306982634894, 120.967233726293"),
                raw_coordinates="24.803306982634894, 120.967233726293",
            ),
            venue_type=VenueType.EXPO_CENTER,
        )

    async def fetch_response(self):
        headers = generate_headers()
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.nhclac.gov.tw/News_actives.aspx?n=5282", cookies=cookies)
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

    await NhClAcRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
