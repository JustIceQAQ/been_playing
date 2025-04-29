import asyncio

import bs4

from app.exhibition.nhrm.parse import NHRMParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, ExhibitionItem
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.suffix_helper import suffix_helper


class NHRMRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NHRMParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="國家人權博物館",
            code_name="NHRM",
            external_link="https://www.nhrm.gov.tw/w/nhrm/ExhibitionA",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "referer": "https://www.nhrm.gov.tw/w/nhrm/ExhibitionA",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://www.nhrm.gov.tw/w/nhrm/ExhibitionA")
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("ul.list-group > li.list-item")

    async def suffix_item_from_file(self, items: list[ExhibitionItem]):
        suffix_data = suffix_helper.get_code_name_items("NHRM")
        for item in items:
            this_suffix: dict | None = suffix_data.get(item.UUID, None)
            if this_suffix:
                for column in item.model_fields.keys():
                    this_column = this_suffix.get(column, None)
                    if this_column:
                        setattr(item, column, this_column)


async def main():
    await NHRMRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
