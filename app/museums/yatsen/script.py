import asyncio
from typing import cast

import bs4

from app.museums.yatsen.parse import YatsenParse
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class YatsenRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = YatsenParse
    retry_on_empty = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.xinyi_63000020,
            fullname="國立國父紀念館",
            code_name="Yatsen",
            external_link="https://www.yatsen.gov.tw/News_actives.aspx?n=7339&sms=13411",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.040205545923655, 121.56033102744308"),
                raw_coordinates="25.040205545923655, 121.56033102744308",
            ),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.yatsen.gov.tw/News_actives.aspx?n=7339&sms=13411")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.find_all("a", {"class": "div-activity"})


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await YatsenRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
