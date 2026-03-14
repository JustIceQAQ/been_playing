import asyncio

import bs4

from app.museums.ncpi.parse import NCPIParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NCPIRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NCPIParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="國家攝影文化中心",
            code_name="NCPI",
            external_link="https://ncpi.ntmofa.gov.tw/News_OnlineExhibitionPic_str.aspx?n=8006&sms=15632",
            branch_coordinates=Coordinate(
                raw_coordinates="25.0468823164654, 121.51432273908243"
            ),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="ncpi.ntmofa.gov.tw")
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [
                client.get(
                    "https://ncpi.ntmofa.gov.tw/News_OnlineExhibitionPic_str.aspx?IsF=1&n=8005&sms=15632",
                    cookies=cookies,
                ),
                client.get(
                    "https://ncpi.ntmofa.gov.tw/News_OnlineExhibitionPic_str.aspx?n=8006&sms=15632",
                    cookies=cookies,
                ),
            ]

            responses = await asyncio.gather(*tasks)
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parseds: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        data = []
        for parsed in parseds:
            data.extend(parsed.select("div.area-essay > div > div > div > a"))
        return data

    async def fetch_items(self, *args, **kwargs):
        return await super().fetch_items(target_domain="https://ncpi.ntmofa.gov.tw/")


async def main():
    await NCPIRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
