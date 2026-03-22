import asyncio

import bs4

from app.museums.jam.parse import JamParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class JamRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = JamParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="忠泰美術館",
            code_name="Jam",
            external_link="https://jam.jutfoundation.org.tw/online-exhibition",
            branch_coordinates=Coordinate(raw_coordinates="25.044509020251724, 121.53731469675466"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="jam.jutfoundation.org.tw", referer="https://jam.jutfoundation.org.tw")

        async with HttpxAsyncClient(headers=headers) as client:
            urls = [
                "https://jam.jutfoundation.org.tw/online-exhibition",
                "https://jam.jutfoundation.org.tw/coming-exhibition",
            ]
            tasks = [
                client.get(
                    url,
                )
                for url in urls
            ]
            responses = await asyncio.gather(*tasks)
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parseds: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        data = []
        for parsed in parseds:
            data.extend(parsed.select("div.view-content > div.views-row"))
        return data


async def main():
    await JamRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
