import asyncio
from typing import cast

import bs4

from app.museums.museumpost.parse import MuseumPostParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class MuseumPostRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = MuseumPostParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="郵政博物館",
            code_name="MuseumPost",
            external_link="https://museum.post.gov.tw/post/Postal_Museum/museum/index.jsp?ID=131&topage=1",
            location_code=Taiwan.taipei.zhongzheng_63000050,
            branch_coordinates=[
                Coordinate(
                    name="本館",
                    geo_point=GeoPoint(
                        raw_coordinates="25.032392367745082, 121.5147638567378",
                    ),
                    raw_coordinates="25.032392367745082, 121.5147638567378",
                    location_code=Taiwan.taipei.zhongzheng_63000050,
                ),
                Coordinate(
                    name="臺北館",
                    geo_point=GeoPoint(
                        raw_coordinates="25.047556287891062, 121.51158812126322",
                    ),
                    raw_coordinates="25.047556287891062, 121.51158812126322",
                    location_code=Taiwan.taipei.zhongzheng_63000050,
                ),
                Coordinate(
                    name="高雄館",
                    geo_point=GeoPoint(
                        raw_coordinates="22.638430558437683, 120.30123181704683",
                    ),
                    raw_coordinates="22.638430558437683, 120.30123181704683",
                    location_code=Taiwan.kaohsiung.sanmin_64000050,
                ),
            ],
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="museum.post.gov.tw", other_headers={"Connection": "keep-alive"})
        cookies = generate_cookies(need_js_ession_id=True)
        async with HttpxAsyncClient(headers=headers) as client:
            target_url = "https://museum.post.gov.tw/post/Postal_Museum/museum/index.jsp?ID=131&topage={to_page}"
            responses = []
            page = 1
            response = await client.get(target_url.format(to_page=page), cookies=cookies)
            translation_data = self.translation().translation_to_object(response.text)
            if translation_data is None:
                return None
            while translation_data.select("ul.part_list > li"):
                responses.append(response.text)
                page += 1
                response = await client.get(target_url.format(to_page=page), cookies=cookies)
                translation_data = self.translation().translation_to_object(response.text)
                if translation_data is None:
                    break

            return responses

    async def fetch_parsed(self):
        parsers = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        items = []
        for parsed in parsers:
            items.extend(parsed.select("ul.part_list > li"))
        return items


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await MuseumPostRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
