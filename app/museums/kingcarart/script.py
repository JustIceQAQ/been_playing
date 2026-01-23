import asyncio
import decimal

import bs4

from app.museums.kingcarart.parse import KingCarArtParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_6


class KingCarArtRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KingCarArtParse

    def set_cache_expire(self) -> int | None:
        return month_6()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="金車文藝中心",
            code_name="KingCarArt",
            external_link="https://www.kingcarart.org.tw/exhibitions/current",
            branch_coordinates=[
                Coordinate(name="臺北承德館", raw_coordinates="25.067779239946375, 121.51865322216524"),
                Coordinate(name="臺北南京館", raw_coordinates="25.052598382305003, 121.5278585635071"),
            ],
            venue_type=VenueType.MUSEUM,
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
        parsed: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        items = []
        for item in parsed:
            items.extend(item.select("ul.ex-list-box > li"))
        return items


async def main():
    await KingCarArtRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
