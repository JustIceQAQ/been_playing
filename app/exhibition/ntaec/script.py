import asyncio

import bs4

from app.exhibition.ntaec.parse import NTAECParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class NTAECRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NTAECParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="國立台灣藝術教育館",
            code_name="NTAEC",
            external_link="https://www.arte.gov.tw/",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "upgrade-insecure-requests": "1",
        }
        cookies = {"ASPSESSIONIDAUCTQQQB": "NEHFIKKCELKMMEJKIMGKIPDP"}
        page_no = 1
        url = "https://www.arte.gov.tw/pro1_exh_nowlist.asp?PageNo=1"
        responses = []
        async with HttpxAsyncClient(headers=headers, cookies=cookies) as client:
            for n in range(3):
                response = await client.get(url, params={"PageNo": page_no + n})
                responses.append(response.text)
        return responses

    async def fetch_parsed(self):
        item_data = []
        parsed: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        for p in parsed:
            items = p.select("div.user-postes.wow")
            item_data.extend(items)
        return item_data


async def main():
    await NTAECRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
