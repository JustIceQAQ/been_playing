import asyncio

from typing import cast
from app.museums.tycg.parse import TyCgParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType

from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage

from helpers.crawler.niquests.helper import NiquestsAsyncSession

from selectolax.lexbor import LexborNode
from helpers.translation.selectolax import SelectolaxTranslation


class TyCgRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = TyCgParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.TAOYUAN_CITY,
            fullname="桃園市立大溪木藝生態博物館",
            code_name="TyCg",
            external_link="https://wem.tycg.gov.tw/",
            branch_coordinates=Coordinate(raw_coordinates="24.880817497601956, 121.28684365533006"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(referer="https://wem.tycg.gov.tw/", host="wem.tycg.gov.tw")
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with NiquestsAsyncSession(headers=headers, timeout=120) as client:
            response = await client.get("https://wem.tycg.gov.tw/News_Photo.aspx?n=9676&sms=13653", cookies=cookies)
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        pages = parsed.css("div.group-list.page-block div.area-figure a")
        return pages


async def main():
    await TyCgRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
