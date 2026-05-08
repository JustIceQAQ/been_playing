import asyncio

import bs4

from app.museums.kingcarart.parse import KingCarArtParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_6
from typing import cast


class KingCarArtRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KingCarArtParse

    def set_cache_expire(self) -> int | None:
        return month_6()

    def set_information(self) -> "Information":
        return Information(
            fullname="金車文藝中心",
            code_name="KingCarArt",
            external_link="https://www.kingcarart.org.tw/exhibitions/current",
            branch_coordinates=[
                Coordinate(
                    name="臺北承德館",
                    raw_coordinates="25.067779239946375, 121.51865322216524",
                    location_code=Taiwan.taipei.zhongzheng_63000050,
                ),
                Coordinate(
                    name="臺北南京館",
                    raw_coordinates="25.052598382305003, 121.5278585635071",
                    location_code=Taiwan.taipei.datong_63000060,
                ),
            ],
            venue_type=VenueType.EXPO_CENTER,
        )

    async def fetch_response(self):
        target_url = (
            "https://www.kingcarart.org.tw/exhibitions/current?"
            "nanjing=true"
            "&chengde=true"
            "&yuanshan=true"
            "&page={page}"
        )
        headers = generate_headers()
        responses = []
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(target_url.format(page=1))
            responses.append(response.text)
            parsed = self.translation().translation_to_object(response.text)
            get_page_number = len(parsed.select("div.pagin-box > div.page-link"))
            for page_flag in range(2, get_page_number + 1):
                sub_response = await client.get(target_url.format(page=page_flag))
                responses.append(sub_response.text)
        return responses

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        items = []
        for item in parsed:
            items.extend(item.select("ul.ex-list-box > li"))
        return items


async def main():
    await KingCarArtRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
