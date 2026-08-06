import asyncio
from typing import cast

import bs4

from app.galleries.whitestone.parse import WhiteStoneParse
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class WhiteStoneRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = WhiteStoneParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.neihu_63000100,
            fullname="白石畫廊",
            code_name="WhiteStone",
            external_link="https://www.whitestone-gallery.com/zh-hant",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.081886335785196, 121.5655333509274"),
                raw_coordinates="25.081886335785196, 121.5655333509274",
            ),
            venue_type=VenueType.GALLERY,
        )

    async def fetch_response(self):
        urls = [
            "https://www.whitestone-gallery.com/zh-hant/blogs/exhibitions/tagged/location_taipei+current",
            "https://www.whitestone-gallery.com/zh-hant/blogs/exhibitions/tagged/location_taipei+upcoming",
        ]
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            responses = await asyncio.gather(*[client.get(url) for url in urls])
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        datas = []
        for p in parsed:
            datas.extend(p.select("div.wsg-exhibition-card"))
        return datas


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await WhiteStoneRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
