import asyncio
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.momatainan.parse import MoMaTainanParse
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_cookies, generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3


class MoMaTainanRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = MoMaTainanParse
    use_suffix_item_from_file_func = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.tainan.west_central_67000370,
            fullname="臺南國家美術館",
            code_name="MoMaTainan",
            external_link="https://www.momatainan.gov.tw/News2.aspx?n=9532&sms=16214",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="22.990673587866652, 120.20223840277899"),
                raw_coordinates="22.990673587866652, 120.20223840277899",
            ),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with NiquestsAsyncSession(headers=headers) as client:
            urls = [
                "https://www.momatainan.gov.tw/News2.aspx?n=9532&sms=16214",
                "https://www.momatainan.gov.tw/News2.aspx?n=9533&sms=16215",
            ]
            responses = await asyncio.gather(*[client.get(url, cookies=cookies) for url in urls])
        return [response.text for response in responses]

    async def fetch_parsed(self):
        items = []
        parsed = cast(list[LexborNode], await super().fetch_parsed())
        for p in parsed:
            items.extend(p.css("div.group-list ul li div.area-essay a"))
        return items


async def main():
    from helpers.cache import none_cache
    from helpers.image_hosting import none_image_hosting

    await MoMaTainanRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
