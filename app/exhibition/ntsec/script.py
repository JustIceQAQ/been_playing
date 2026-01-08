import asyncio

import bs4
import httpx
from dateutil.relativedelta import relativedelta

from app.exhibition.ntsec.format.address import get_page_address
from app.exhibition.ntsec.parse import NtSecParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, ExhibitionItem, Coordinate
from helpers.storage.symbol import TaiwanCity
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import datetime_now, month_3, get_asyncio_rate_limit


class NtSecRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NtSecParse
    use_suffix_item_from_url_auto = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="國立臺灣科學教育館",
            code_name="NtSec",
            external_link="https://www.ntsec.gov.tw/article/list.aspx?a=25",
            branch_coordinates=Coordinate(raw_coordinates="25.096328164549, 121.51649185712368"),
        )

    def get_this_headers(self) -> dict:
        return get_headers(host="www.ntsec.gov.tw")

    async def fetch_response(self):
        headers = self.get_this_headers()
        s_datetime = datetime_now()
        s_date = s_datetime.strftime("%Y-%m-%d")
        e_datetime = s_datetime + relativedelta(months=2)
        e_date = e_datetime.strftime("%Y-%m-%d")
        url_template = "https://www.ntsec.gov.tw/article/list.aspx?a=25&s_date={s_date}&e_date={e_date}"
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                url_template.format(s_date=s_date, e_date=e_date)
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("#MainContent_divListItem > a")

    async def fetch_items(self, *args, **kwargs):
        return await super().fetch_items(target_domain="https://www.ntsec.gov.tw")

    async def suffix_data(self, client: httpx.AsyncClient, item: ExhibitionItem):
        has_address_cache = await self.cache.aget(f"{item.UUID}-address")
        if has_address_cache:
            item.address = has_address_cache
            return
        response = await client.get(item.source_url)
        soup = self.translation().translation_to_object(response.text)
        exhibition_location = get_page_address(soup)
        await self.cache.aset(f"{item.UUID}-address", exhibition_location, month_3())
        item.address = exhibition_location

    async def suffix_item_from_url_auto(self, items: list[ExhibitionItem]):
        headers = self.get_this_headers()
        asyncio_limit = get_asyncio_rate_limit(3, 30)
        async with HttpxAsyncClient(headers=headers) as client, asyncio_limit:
            await asyncio.gather(*[self.suffix_data(client, item) for item in items])


async def main():
    await NtSecRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
