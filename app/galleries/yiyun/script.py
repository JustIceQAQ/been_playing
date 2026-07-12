import asyncio

import bs4

from app.galleries.yiyun.parse import YiYunParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3

from typing import cast


class YiYunRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = YiYunParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="異雲書屋",
            code_name="YiYun",
            external_link="https://www.yiyun-art.com/",
            branch_coordinates=[
                Coordinate(
                    location_code=Taiwan.taipei.daan_63000030,
                    name="青田館",
                    geo_point=GeoPoint(
                        raw_coordinates="25.027213880907816, 121.53055350558525",
                    ),
                    raw_coordinates="25.027213880907816, 121.53055350558525",
                ),
                Coordinate(
                    location_code=Taiwan.taipei.daan_63000030,
                    name="金華館",
                    geo_point=GeoPoint(
                        raw_coordinates="25.028205131565272, 121.53223852023619",
                    ),
                    raw_coordinates="25.028205131565272, 121.53223852023619",
                ),
            ],
            venue_type=VenueType.GALLERY,
        )

    async def fetch_response(self):
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.yiyun-art.com/exhibitions")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        current = parsed.find("div", {"id": "current"})
        following = parsed.find("div", {"id": "following"})
        followings = following.find_all("a", {"class": "exhibition-list"})
        if current is not None:
            followings.append(current)
        return followings


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await YiYunRunner().run(none_cache, none_image_hosting, develop_mode=True)


if __name__ == "__main__":
    asyncio.run(main())
