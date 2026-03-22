import asyncio

import bs4
from app.museums.yatsen.parse import YatsenParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class YatsenRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = YatsenParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="國立國父紀念館",
            code_name="Yatsen",
            external_link="https://www.yatsen.gov.tw/News_actives.aspx?n=7339&sms=13411",
            branch_coordinates=Coordinate(raw_coordinates="25.040205545923655, 121.56033102744308"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.yatsen.gov.tw/News_actives.aspx?n=7339&sms=13411")
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.find_all("a", {"class": "div-activity"})

    async def items_check(self):
        pass


async def main():
    await YatsenRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
