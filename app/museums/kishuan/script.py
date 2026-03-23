import asyncio
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.kishuan.parse import KiShuAnParse
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class KiShuAnRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = KiShuAnParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="紀州庵文學森林",
            code_name="KiShuAn",
            external_link="https://kishuan.org.tw/activity.htm",
            branch_coordinates=Coordinate(raw_coordinates="25.021773564949243, 121.5206021625705"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            host="kishuan.org.tw",
            referer="https://kishuan.org.tw/activity.htm",
            need_upgrade_insecure_requests=True,
        )
        async with NiquestsAsyncSession(headers=headers) as client:
            response = await client.get("https://kishuan.org.tw/activity.htm")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        qq = parsed.css("div.activityList > div.wrap")
        return qq


async def main():
    await KiShuAnRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
