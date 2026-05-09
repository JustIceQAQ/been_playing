import asyncio

import bs4

from app.museums.nmh.parse import NmhParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3

from typing import cast


class NmhRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NmhParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.zhongzheng_63000050,
            fullname="國立歷史博物館",
            code_name="Nmh",
            external_link="https://www.nmh.gov.tw/News_Actives_photo.aspx?n=6983&sms=13323",
            branch_coordinates=Coordinate(raw_coordinates="25.0317350368833, 121.51118866791836"),
            venue_type=VenueType.MEMORIAL,
        )

    async def fetch_response(self):
        headers = generate_headers(
            host="www.nmh.gov.tw",
            referer="https://www.nmh.gov.tw/News_Actives_photo.aspx?n=6983&sms=13323",
        )

        url_template = "https://www.nmh.gov.tw/News_Actives_photo.aspx?n={n}&sms=13323"
        numbers = (
            6984,
            6983,
        )

        async with HttpxAsyncClient(headers=headers) as client:
            responses = await asyncio.gather(*[client.get(url_template.format(n=number)) for number in numbers])
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        datas = []
        for p in parsed:
            datas.extend(p.select("div.area-figure.page-figure"))
        return datas


async def main():
    await NmhRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
