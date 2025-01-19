import asyncio
import secrets

import bs4

from app.exhibition.ncpi.parse import NCPIParse
from helpers.cache.none.helper import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NCPIRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NCPIParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="國家攝影文化中心",
            code_name="NCPI",
            external_link="https://ncpi.ntmofa.gov.tw/News_OnlineExhibitionPic_str.aspx?n=8006&sms=15632",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "Host": "ncpi.ntmofa.gov.tw",
            "Cookie": f"ASP.NET_SessionId={secrets.token_hex(12)}",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [
                client.get(
                    "https://ncpi.ntmofa.gov.tw/News_OnlineExhibitionPic_str.aspx?IsF=1&n=8005&sms=15632"
                ),
                client.get(
                    "https://ncpi.ntmofa.gov.tw/News_OnlineExhibitionPic_str.aspx?n=8006&sms=15632"
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
