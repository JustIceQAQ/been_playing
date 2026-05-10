import asyncio
from typing import cast

import bs4

from app.museums.ttcsec.parse import TtCsEcParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class TtCsEcRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TtCsEcParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taitung.taitung_10014010,
            fullname="國立臺東生活美學館",
            code_name="ttcsec",
            external_link="https://www.ttcsec.gov.tw/",
            branch_coordinates=Coordinate(raw_coordinates="22.755456248316037, 121.15105139554878"),
            venue_type=VenueType.EXPO_CENTER,
        )

    async def fetch_response(self):
        headers = generate_headers()
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://www.ttcsec.gov.tw/News_Actives_photo.aspx?n=2387&sms=11896",
                cookies=cookies,
            )
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        items = parsed.find("div", {"class": "group-list page-block"})
        if items is None:
            return None
        datas = items.find_all("a", {"class": "div-activity"})
        return datas


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image.none.helper import NoneImage

    await TtCsEcRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
