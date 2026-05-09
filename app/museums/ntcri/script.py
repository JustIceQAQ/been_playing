import asyncio
from typing import Any, cast

from app.museums.ntcri.parse import NTCRIParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class NTCRIRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = NTCRIParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="國立台灣工藝研究發展中心",
            code_name="NTCRI",
            external_link=(
                "https://tcdbdata.ntcri.gov.tw/api/cms/exhibition?"
                "limit=50"
                "&offset=0"
                "&query=null"
                "&sort=sort"
                "&order=asc"
            ),
            location_code=Taiwan.taipei.zhongzheng_63000050,
            branch_coordinates=[
                Coordinate(
                    location_code=Taiwan.taipei.zhongzheng_63000050,
                    name="臺北當代工藝設計分館",
                    raw_coordinates="25.03210292140622, 121.51234399386772",
                ),
            ],
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            host="tcdbdata.ntcri.gov.tw",
            origin="https://www.ntcri.gov.tw",
            referer="https://www.ntcri.gov.tw/",
            other_headers={
                "access_token": "b550b95f-ce44-4684-968b-298b0f5ad483",
                "accept": "application/json, text/plain, */*",
            },
        )
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://tcdbdata.ntcri.gov.tw/api/cms/exhibition?limit=50&offset=0&query=null&sort=sort&order=asc"
            )
            response.raise_for_status()
        return response.json()["rows"]

    async def fetch_parsed(self):
        parsed = cast(list[dict[str, Any]], await super().fetch_parsed())
        return parsed


async def main():
    await NTCRIRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
