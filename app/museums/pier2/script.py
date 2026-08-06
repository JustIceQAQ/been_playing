import asyncio
import datetime
from typing import cast

from app.museums.pier2.parse import Pier2Parse
from helpers.crawler.wreq.helper import WReqAsyncClient
from helpers.headers_helper import generate_cookies, generate_headers
from helpers.runner.helper import RunnerInit
from helpers.sniff_error import safe_json
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class Pier2Runner(RunnerInit):
    translation = JsonTranslation
    use_parse = Pier2Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.kaohsiung.yancheng_64000010,
            fullname="駁二藝術特區",
            code_name="Pier2",
            external_link="https://pier2.org/exhibition/list/all/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="22.620055196410377, 120.28155879030746"),
                raw_coordinates="22.620055196410377, 120.28155879030746",
            ),
            venue_type=VenueType.CREATIVE_PARK,
        )

    async def fetch_response(self):
        headers = generate_headers(
            referer="https://pier2.org/exhibition/list/all/",
            origin="https://pier2.org",
            x_requested_with="XMLHttpRequest",
        )
        cookies = generate_cookies(need_phpsessid=True)
        params = {
            "type": "exhibition",
            "date": f"{datetime.date.today():%Y-%m-%d}",
        }
        async with WReqAsyncClient(headers=headers, use_proxies=True) as client:
            response = await client.post("https://pier2.org/api/eventList.php", query=params, cookies=cookies)
        return await safe_json(response, "Pier2")

    async def fetch_parsed(self):
        parsed = cast(dict, await super().fetch_parsed())
        return parsed.get("list", [])


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await Pier2Runner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
