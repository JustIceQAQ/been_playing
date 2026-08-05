import asyncio
from typing import cast

import bs4

from app.museums.ntaec.parse import NTAECParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NTAECRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NTAECParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.zhongzheng_63000050,
            fullname="國立台灣藝術教育館",
            code_name="NTAEC",
            external_link="https://www.arte.gov.tw/pro1_exh_nowlist.asp",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.03249656295196, 121.51211159386773"),
                raw_coordinates="25.03249656295196, 121.51211159386773",
            ),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(need_upgrade_insecure_requests=True)
        page_no = 1
        url = "https://www.arte.gov.tw/pro1_exh_nowlist.asp"
        responses = []
        async with HttpxAsyncClient(headers=headers) as client:
            for n in range(3):
                response = await client.get(url, params={"PageNo": page_no + n})
                responses.append(response.text)
        return responses

    async def fetch_parsed(self):
        item_data = []
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        for p in parsed:
            items = p.select("div.single-page div.user-postes div.row")
            item_data.extend(items)
        return item_data


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await NTAECRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
