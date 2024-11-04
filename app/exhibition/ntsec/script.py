import asyncio

import bs4
from dateutil.relativedelta import relativedelta

from app.exhibition.ntsec.parse import NtSecParse
from helpers.cache.none.helper import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import datetime_now, month_3


class NtSecRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NtSecParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="國立臺灣科學教育館",
            code_name="NtSec",
            external_link="https://www.ntsec.gov.tw/article/list.aspx?a=25",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "Host": "www.ntsec.gov.tw",
        }
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


async def main():
    await NtSecRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
