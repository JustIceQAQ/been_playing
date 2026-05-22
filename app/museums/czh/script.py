import asyncio
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.czh.parse import CZHParse
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_cookies, generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3


class CZHRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = CZHParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.changhua.changhua_10007010,
            fullname="彰化藝術館",
            code_name="CZH",
            external_link="https://www.bocach.gov.tw/News.aspx?n=1397&sms=10815&_Query=36343dc0-af59-428f-93d4-5eb4382a3baf",
            branch_coordinates=Coordinate(raw_coordinates="24.079288468869468, 120.54543250906565"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="www.bocach.gov.tw")
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with NiquestsAsyncSession(headers=headers) as client:
            response = await client.get(
                "https://www.bocach.gov.tw/News.aspx?n=1397&sms=10815&_Query=36343dc0-af59-428f-93d4-5eb4382a3baf",
                cookies=cookies,
            )
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        return parsed.css("div.area-table table tbody tr")


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await CZHRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
