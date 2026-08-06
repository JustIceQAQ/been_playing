import asyncio
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.tycg.parse import TyCgParse
from helpers.crawler.headers_helper import generate_cookies, generate_headers
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3


class TyCgRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = TyCgParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taoyuan.daxi_68000030,
            fullname="桃園市立大溪木藝生態博物館",
            code_name="TyCg",
            external_link="https://wem.tycg.gov.tw/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="24.880817497601956, 121.28684365533006"),
                raw_coordinates="24.880817497601956, 121.28684365533006",
            ),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(referer="https://wem.tycg.gov.tw/", host="wem.tycg.gov.tw")
        cookies = generate_cookies(
            need_asp_net_session_id=True,
            other_cookies={
                "font-size-": "medium",
            },
        )
        async with NiquestsAsyncSession(headers=headers, use_proxy=True) as client:
            response = await client.get(
                "https://wem.tycg.gov.tw/News_Photo.aspx?n=9676&sms=13653",
                cookies=cookies,
            )
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        pages = parsed.css("div.group-list.page-block div.area-figure a")
        return pages


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await TyCgRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
