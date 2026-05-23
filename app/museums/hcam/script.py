import asyncio
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.hcam.parse import HCAMParse
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_cookies, generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3, get_date


class HCAMRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = HCAMParse
    retry_on_empty = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.hsinchu_city.east_10018010,
            fullname="新竹市美術館",
            code_name="HCAM",
            external_link="https://culture.hccg.gov.tw/ch/home.jsp?id=452&parentpath=0,145,154&mcustomize=activity_list.jsp",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="24.806516978000005, 120.97006803902325"),
                raw_coordinates="24.806516978000005, 120.97006803902325",
            ),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            host="culture.hccg.gov.tw",
        )
        cookies = generate_cookies(need_js_ession_id=True)

        async with NiquestsAsyncSession(headers=headers) as client:
            data = {
                "id": "452",
                "parentpath": "0,145,154",
                "mcustomize": "activity_list.jsp",
                "qptdatechina": get_date.now_format_to_roc_era_ios,
                "qptdate": get_date.now_format_to_ios,
                "keyword": "[展覽]",
                "page": "1",
                "pagesize": "10",
            }
            response = await client.post(
                "https://culture.hccg.gov.tw/ch/home.jsp",
                cookies=cookies,
                params={"id": "452", "parentpath": "0,145,154", "mcustomize": "activity_list.jsp"},
                data=data,
            )
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        items = parsed.css("#css_table div.list_list")
        ok_items = []
        for item in items:
            list_title = item.css_first("div.list_title").text(strip=True)
            if "暫無" not in list_title:
                ok_items.append(item)
        return ok_items


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await HCAMRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
