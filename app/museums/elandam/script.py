import asyncio
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.elandam.parse import ELandAMParse
from helpers.crawler.headers_helper import generate_cookies, generate_headers
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3


class ELandAMRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = ELandAMParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.yilan.yilan_10002010,
            fullname="宜蘭美術館",
            code_name="ELandAM",
            external_link="https://ymoa.e-land.gov.tw/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="24.7550562904822, 121.75175462425617"),
                raw_coordinates="24.7550562904822, 121.75175462425617",
            ),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            referer="https://ymoa.e-land.gov.tw/News2.aspx?n=5180&sms=14712",
            host="ymoa.e-land.gov.tw",
        )
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with NiquestsAsyncSession(headers=headers) as client:
            response = await client.get("https://ymoa.e-land.gov.tw/News2.aspx?n=2261&sms=14713", cookies=cookies)
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        items = parsed.css("div.group-list li div.area-essay a")
        return items


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await ELandAMRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
