import asyncio

import bs4

from app.exhibition.nmh.parse import NmhParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NmhRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NmhParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="國立歷史博物館",
            code_name="Nmh",
            external_link="https://www.nmh.gov.tw/News_Actives_photo.aspx?n=6983&sms=13323",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "Host": "www.nmh.gov.tw",
            "Referer": "https://www.nmh.gov.tw/News_Actives_photo.aspx?n=6983&sms=13323",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://www.nmh.gov.tw/News_Actives_photo.aspx?n=6983&sms=13323"
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div.area-figure.page-figure")


async def main():
    await NmhRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
