import asyncio
from typing import cast

import bs4

from app.museums.ntmofa.parse import NtMofaParse
from helpers.crawler.headers_helper import generate_cookies, generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NtMofaRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NtMofaParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taichung.west_66000040,
            fullname="國立臺灣美術館",
            code_name="NtMofa",
            external_link="https://www.ntmofa.gov.tw/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="24.141372397797248, 120.66338819860081"),
                raw_coordinates="24.141372397797248, 120.66338819860081",
            ),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        cookies = generate_cookies(need_asp_net_session_id=True)
        urls = [
            "https://www.ntmofa.gov.tw/News_Actives_photo.aspx?n=1462&sms=11893",
            "https://www.ntmofa.gov.tw/News_Actives_photo.aspx?n=1464&sms=11893",
        ]
        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [client.get(url, cookies=cookies) for url in urls]
            responses = await asyncio.gather(*tasks)
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        data = []
        for p in parsed:
            element = p.select("div#CCMS_Content a")
            if element:
                data.extend(element[1:])
        return data


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await NtMofaRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
