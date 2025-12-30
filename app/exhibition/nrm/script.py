import asyncio
import decimal

import bs4
from app.exhibition.nrm.parse import NrmParse
from helpers.headers_helper import get_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class NrmRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NrmParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="國家鐵道博物館",
            code_name="Nrm",
            external_link="https://www.nrm.gov.tw/News_actives.aspx?n=3325&sms=13412",
            branch_coordinates=Coordinate(raw_coordinates="25.04759981549798, 121.56476041209898"),
        )

    async def fetch_response(self):
        headers = get_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://www.nrm.gov.tw/News_actives.aspx?n=3325&sms=13412"
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.find_all("a", {"class": "div-activity"})


async def main():
    await NrmRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
