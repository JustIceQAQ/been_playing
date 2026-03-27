import asyncio
import datetime
from typing import cast

from app.museums.pier2.parse import Pier2Parse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class Pier2Runner(RunnerInit):
    translation = JsonTranslation
    use_parse = Pier2Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.KAOHSIUNG_CITY,
            fullname="駁2藝術特區",
            code_name="Pier2",
            external_link="https://pier2.org/exhibition/list/all/",
            branch_coordinates=Coordinate(raw_coordinates="22.620055196410377, 120.28155879030746"),
            venue_type=VenueType.MUSEUM,
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
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post("https://pier2.org/api/eventList.php", params=params, cookies=cookies)
        return response.json()

    async def fetch_parsed(self):
        parsed = cast(dict, await super().fetch_parsed())
        return parsed.get("list", [])


async def main():
    await Pier2Runner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
