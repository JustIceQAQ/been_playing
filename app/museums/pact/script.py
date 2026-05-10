import asyncio
import urllib.parse
from app.museums.pact.parse import PactParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3

from typing import cast


class PactRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = PactParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.songshan_63000010,
            fullname="台北偶戲館",
            code_name="PACT",
            external_link="https://www.pact.taipei/exhibition_list.aspx?p=1&ps=10&t=all",
            branch_coordinates=Coordinate(raw_coordinates="25.04792075475668, 121.56141474093504"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        aspx = "https://www.pact.taipei/exhibition_list.aspx"
        headers = generate_headers(
            referer=f"{aspx}?p=1&ps=10&t=all",
            origin="https://www.pact.taipei",
            host="www.pact.taipei",
            x_requested_with="XMLHttpRequest",
        )
        data = {
            "q": "get",
            "r": "0.9",
            "t": "all",
            "data": urllib.parse.quote('{"p":1,"ps":10,"t":"all"}'),
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post(aspx, data=data)
            response.raise_for_status()
        return response.json()

    async def fetch_parsed(self):
        parsed = cast(dict, await super().fetch_parsed())
        return parsed["list"]["items"]


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImage

    await PactRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
