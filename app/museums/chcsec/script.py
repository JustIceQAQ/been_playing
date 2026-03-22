import asyncio

import bs4

from app.museums.chcsec.parse import ChCsEcParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class ChCsEcRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = ChCsEcParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.changhua_county,
            fullname="國立彰化生活美學館",
            code_name="chcsec",
            external_link="https://www.chcsec.gov.tw/News_actives.aspx?n=4020&sms=13269&_Query=b7c33695-58eb-4e1d-82e1-5e73654b385a&_CSN=",
            branch_coordinates=Coordinate(raw_coordinates="24.076669410098226, 120.55732233791466"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://www.chcsec.gov.tw/News_actives.aspx?n=4020&sms=13269",
                cookies=cookies,
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        items = parsed.find("div", {"class": "group-list message"})
        if items is None:
            return None
        return items.find_all("a", {"class": "div-activity"})


async def main():
    await ChCsEcRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
