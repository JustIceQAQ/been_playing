import asyncio
from typing import cast

import bs4

from app.museums.cksmh.parse import CKSMHParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GoogleMaps, GeoPoint
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class CKSMHRunner(RunnerInit):
    """中正紀念堂"""

    translation = BeautifulSoupTranslation
    use_parse = CKSMHParse
    output_ics = True
    output_rss = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.zhongzheng_63000050,
            fullname="中正紀念堂",
            code_name="CKSMH",
            external_link="https://www.cksmh.gov.tw/Default.aspx",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(
                    raw_coordinates="25.035657453594702, 121.52023682270445",
                ),
                raw_coordinates="25.035657453594702, 121.52023682270445",
                google_maps=GoogleMaps(plus_code="2GPC+63 中正區 臺北市"),
            ),
            venue_type=VenueType.MEMORIAL,
        )

    async def fetch_response(self) -> str:
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.cksmh.gov.tw/News_Actives_photo.aspx?n=6067&sms=14954")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        div = parsed.select("div.group-list.page-block div.area-figure")
        return div


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await CKSMHRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
