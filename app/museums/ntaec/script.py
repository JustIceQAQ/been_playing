import asyncio

import bs4

from app.museums.ntaec.parse import NTAECParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage

from typing import cast


class NTAECRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NTAECParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.zhongzheng_63000050,
            fullname="國立台灣藝術教育館",
            code_name="NTAEC",
            external_link="https://www.arte.gov.tw/",
            branch_coordinates=Coordinate(raw_coordinates="25.03249656295196, 121.51211159386773"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(need_upgrade_insecure_requests=True)
        cookies = {"ASPSESSIONIDAUCTQQQB": "NEHFIKKCELKMMEJKIMGKIPDP"}
        page_no = 1
        url = "https://www.arte.gov.tw/pro1_exh_nowlist.asp?PageNo=1"
        responses = []
        async with HttpxAsyncClient(headers=headers) as client:
            for n in range(3):
                response = await client.get(url, params={"PageNo": page_no + n}, cookies=cookies)
                responses.append(response.text)
        return responses

    async def fetch_parsed(self):
        item_data = []
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        for p in parsed:
            items = p.select("div.user-postes.wow")
            item_data.extend(items)
        return item_data


async def main():
    await NTAECRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
