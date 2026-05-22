import asyncio
import datetime
from typing import cast

from app.museums.taipeizoo.parse import TaipeiZooParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import ExhibitionItem, Information
from helpers.storage.coordinate import Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import get_timezone, month_3


class TaipeiZooRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = TaipeiZooParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="臺北市立動物園",
            code_name="TaipeiZoo",
            external_link="https://www.zoo.gov.taipei/",
            branch_coordinates=Coordinate(raw_coordinates="24.998626027698112, 121.58097916355628"),
            location_code=Taiwan.taipei.wenshan_63000080,
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="www.zoo.gov.taipei")
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.zoo.gov.taipei/OpenData.aspx?SN=91751F280F16DF38")
            response.raise_for_status()
        return response.json()

    async def fetch_parsed(self):
        parsed = cast(list, await super().fetch_parsed())
        return parsed

    async def fetch_items(self, *args, **kwargs) -> list[ExhibitionItem]:
        items = await super().fetch_items(*args, **kwargs)
        today = datetime.datetime.now(tz=get_timezone()).replace(hour=0, minute=0, second=0, microsecond=0)
        two_years_ago = today - datetime.timedelta(days=730)
        result = []
        for item in items:
            date_type = item.extract_date_type()
            if date_type == 2:
                continue
            end_date = item.extract_end_date()
            if end_date is not None and end_date < today:
                continue
            if date_type == 3:
                start_date = item.extract_start_date()
                if start_date is not None and start_date < two_years_ago:
                    continue
            result.append(item)
        return result


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await TaipeiZooRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
