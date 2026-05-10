import asyncio
from typing import cast

import bs4

from app.museums.ntcceramics.parse import NtcCeramicsParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NtcCeramicsRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NtcCeramicsParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.new_taipei.yingge_65000080,
            fullname="新北市立鶯歌陶瓷博物館",
            code_name="NtcCeramics",
            external_link="https://www.ceramics.ntpc.gov.tw/",
            branch_coordinates=Coordinate(raw_coordinates="24.949406697655782, 121.35203269093292"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            x_requested_with="XMLHttpRequest",
            referer="https://www.ceramics.ntpc.gov.tw/xmdoc?xsmsid=0J148497613881029302",
            origin="https://www.ceramics.ntpc.gov.tw",
            host="www.ceramics.ntpc.gov.tw",
        )
        async with HttpxAsyncClient(headers=headers) as client:
            html_response = await client.get("https://www.ceramics.ntpc.gov.tw/xmdoc?xsmsid=0J148497613881029302")
            soup = BeautifulSoupTranslation().translation_to_object(
                html_response.text,
            )
            request_verification_token = soup.find("input", {"name": "__RequestVerificationToken"})["value"]
            xsms_id = soup.find("input", {"name": "XsmSId"})["value"]
            condss_id = soup.find("input", {"name": "CondsSId"})["value"]

            data = {
                "__RequestVerificationToken": request_verification_token,
                "XsmSId": xsms_id,
                "CondsSId": condss_id,
                "ExecAction": "Q",
                "IndexOfPages": 1,
                "PageSize": 50,
            }
            xmdoc_response = await client.post("https://www.ceramics.ntpc.gov.tw/xmdoc/indexaction", data=data)
        return xmdoc_response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        return parsed.select("div.item")


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await NtcCeramicsRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
