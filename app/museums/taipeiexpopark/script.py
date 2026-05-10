import asyncio
import uuid

import bs4

from app.museums.taipeiexpopark.parse import TaipeiExPoParkParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import get_ad_to_roc_era, get_date_now, month_3
from typing import cast


class TaipeiExPoParkRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TaipeiExPoParkParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.zhongshan_63000040,
            fullname="花博公園",
            code_name="TaipeiExPoPark",
            external_link="https://www.expopark.taipei/News_Exhibition.aspx?n=247&sms=9029",
            branch_coordinates=Coordinate(raw_coordinates="25.069720986746507, 121.52071496978188"),
            venue_type=VenueType.CREATIVE_PARK,
        )

    async def fetch_response(self):
        headers = generate_headers(
            origin="https://www.expopark.taipei",
            referer="https://www.expopark.taipei/News_Exhibition.aspx?n=247&sms=9029",
        )
        cookies = generate_cookies(need_asp_net_session_id=True, other_cookies={"font-size-": "medium"})
        params = {
            "n": 247,
            "sms": 9029,
            "page": 1,
            "PageSize": 100,
            "_Query": str(uuid.uuid4()),
            "Create": 1,
        }
        this_date = get_date_now()
        this_date_format = this_date.strftime("%Y/%m/%d")
        this_roc_era = get_ad_to_roc_era(this_date.year)
        this_date_format = this_date_format.replace(str(this_date.year), str(this_roc_era))

        data = {
            "jNewsModule_field_SDate4": this_date_format,
            "jNewsModule_BtnSend": "送出查詢",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post(
                "https://www.expopark.taipei/News_Exhibition.aspx",
                params=params,
                data=data,
                cookies=cookies,
            )
            response.raise_for_status()
        return response.text

    async def fetch_parsed(self):
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        item = parsed.select_one("div.page-block").select("div.event-list")
        return item


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImage

    await TaipeiExPoParkRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
