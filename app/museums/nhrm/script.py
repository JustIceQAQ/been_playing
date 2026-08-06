import asyncio
from typing import cast

import bs4

from app.museums.nhrm.parse import NHRMParse
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NHRMRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NHRMParse
    use_suffix_item_from_file_func = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.new_taipei.xindian_65000060,
            fullname="國家人權博物館",
            code_name="NHRM",
            external_link="https://www.nhrm.gov.tw/w/nhrm/ExhibitionA",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="24.987027946019857, 121.53208236236004"),
                raw_coordinates="24.987027946019857, 121.53208236236004",
            ),
            venue_type=VenueType.MEMORIAL,
        )

    async def fetch_response(self):
        headers = generate_headers(referer="https://www.nhrm.gov.tw/w/nhrm/ExhibitionA")
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.nhrm.gov.tw/w/nhrm/ExhibitionA")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("ul.list-group > li.list-item")


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await NHRMRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
