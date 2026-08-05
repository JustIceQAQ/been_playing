import asyncio
import urllib.parse
from typing import cast

from app.museums.redhouse.parse import RedHouseParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class RedHouseRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = RedHouseParse
    is_sort: bool = False
    use_suffix_item_from_file_func = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.wanhua_63000070,
            fullname="西門紅樓",
            code_name="RedHouse",
            external_link="https://www.redhouse.taipei/index.aspx",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.042286045915937, 121.50683773908234"),
                raw_coordinates="25.042286045915937, 121.50683773908234",
            ),
            venue_type=VenueType.MEMORIAL,
        )

    async def fetch_response(self):
        aspx = "https://www.redhouse.taipei/events.aspx"
        headers = generate_headers(
            host="www.redhouse.taipei",
            origin="https://www.redhouse.taipei",
            referer=aspx,
            x_requested_with="XMLHttpRequest",
        )
        data = {
            "q": "get",
            "r": "0.001",
            "t": "all",
            "data": urllib.parse.quote('{"ps":10,"p":1,"Kind":"展覽","Title":""}'),
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(aspx, params=data)
            response.raise_for_status()
        return response.json()

    async def fetch_parsed(self):
        parsed = cast(dict, await super().fetch_parsed())
        return parsed["items"]


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await RedHouseRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
