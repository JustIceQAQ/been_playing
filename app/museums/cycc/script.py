import asyncio
from typing import cast

from selectolax.lexbor import LexborHTMLParser

from app.museums.cycc.parse import CyccParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Coordinate, Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3

BASE_URL = "https://cycc.org.tw"


class CyccRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = CyccParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> Information:
        return Information(
            fullname="中原文創園區",
            code_name="Cycc",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(raw_coordinates="24.963707640336903, 121.24146770674547"),
            location_code=Taiwan.taoyuan.zhongli_68000020,
            venue_type=VenueType.CREATIVE_PARK,
        )

    async def fetch_response(self):
        headers = generate_headers(host="cycc.org.tw", referer=BASE_URL)
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(f"{BASE_URL}/zh-hant/events")
            response.raise_for_status()
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborHTMLParser, await super().fetch_parsed())
        return parsed.css("div.eventpage-item")


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await CyccRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
