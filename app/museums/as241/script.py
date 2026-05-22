import asyncio
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.as241.parse import AS241Parse
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_cookies, generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import get_date_format_, get_roc_era_format_date_now, month_3


class AS241Runner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = AS241Parse
    use_suffix_item_from_url_auto = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.hsinchu_city.east_10018010,
            fullname="新竹241藝術空間",
            code_name="AS241",
            external_link="https://culture.hccg.gov.tw/ch/home.jsp?id=453&parentpath=0,145,155&mcustomize=activity_list.jsp",
            branch_coordinates=Coordinate(raw_coordinates="24.809865473262477, 120.97641199854829"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            host="culture.hccg.gov.tw",
        )
        cookies = generate_cookies(need_js_ession_id=True)
        async with NiquestsAsyncSession(headers=headers) as client:
            data = {
                "id": "453",
                "parentpath": "0,145,155",
                "mcustomize": "activity_list.jsp",
                "qptdatechina": get_roc_era_format_date_now(),
                "qptdate": get_date_format_(),
                "keyword": "[展覽][241藝術空間]",
                "page": "1",
                "pagesize": "10",
            }
            response = await client.post(
                "https://culture.hccg.gov.tw/ch/home.jsp",
                cookies=cookies,
                params={"id": "453", "parentpath": "0,145,155", "mcustomize": "activity_list.jsp"},
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

    await AS241Runner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
