import asyncio

import bs4

from app.museums.nmtl.parse import NMTLParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class NMTLRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NMTLParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.tainan_city,
            fullname="國立臺灣文學館",
            code_name="NMTL",
            external_link="https://www.nmtl.gov.tw/News_actives.aspx?n=3821&sms=13367",
            branch_coordinates=Coordinate(raw_coordinates="22.992188481194308, 120.20432889300697"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(need_upgrade_insecure_requests=True)
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with HttpxAsyncClient(headers=headers, cookies=cookies) as client:
            response = await client.get("https://www.nmtl.gov.tw/News_actives.aspx?n=3821&sms=13367")
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div.group-list li div.area-essay")


async def main():
    await NMTLRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
