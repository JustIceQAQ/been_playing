import asyncio
from typing import cast

import bs4

from app.museums.nmtl.parse import NMTLParse
from helpers.crawler.headers_helper import generate_cookies, generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NMTLRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NMTLParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.tainan.west_central_67000370,
            fullname="國立臺灣文學館",
            code_name="NMTL",
            external_link="https://www.nmtl.gov.tw/News_actives.aspx?n=3821&sms=13367",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="22.992188481194308, 120.20432889300697"),
                raw_coordinates="22.992188481194308, 120.20432889300697",
            ),
            venue_type=VenueType.MEMORIAL,
        )

    async def fetch_response(self):
        headers = generate_headers(need_upgrade_insecure_requests=True)
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://www.nmtl.gov.tw/News_actives.aspx?n=3821&sms=13367",
                cookies=cookies,
            )
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("div.group-list li div.area-essay")


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await NMTLRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
