import asyncio

import bs4

from app.museums.nhclac.parse import NhClAcParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3

from typing import cast


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
            branch_coordinates=Coordinate(raw_coordinates="24.803306982634894, 120.967233726293"),
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
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await NhClAcRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
