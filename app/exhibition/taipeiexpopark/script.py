import asyncio
import secrets
import uuid

import bs4

from app.exhibition.taipeiexpopark.parse import TaipeiExPoParkParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import ad_to_roc_era, date_now, month_3


class TaipeiExPoParkRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TaipeiExPoParkParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="花博公園",
            code_name="TaipeiExPoPark",
            external_link="https://www.expopark.taipei/News_Exhibition.aspx?n=247&sms=9029",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "origin": "https://www.expopark.taipei",
            "referer": "https://www.expopark.taipei/News_Exhibition.aspx?n=247&sms=9029",
            "cookie": f"ASP.NET_SessionId={secrets.token_hex(12)}; font-size-=medium",
        }
        params = {
            "n": 247,
            "sms": 9029,
            "page": 1,
            "PageSize": 100,
            "_Query": str(uuid.uuid4()),
            "Create": 1,
        }
        this_date = date_now()
        this_date_format = this_date.strftime("%Y/%m/%d")
        this_roc_era = ad_to_roc_era(this_date.year)
        this_date_format = this_date_format.replace(
            str(this_date.year), str(this_roc_era)
        )

        data = {
            "jNewsModule_field_SDate4": this_date_format,
            "jNewsModule_BtnSend": "送出查詢",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post(
                "https://www.expopark.taipei/News_Exhibition.aspx",
                params=params,
                data=data,
            )
            if not (response.is_success or response.is_redirect):
                raise RuntimeError(response.text)

            response2 = await client.get(
                f"{response.next_request.url}&page=1&PageSize=100"
            )
            if not (response2.is_success or response2.is_redirect):
                raise RuntimeError(response.text)

        return response2.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        item = parsed.select_one("div.page-block").select("div.event-list")
        return item


async def main():
    await TaipeiExPoParkRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
