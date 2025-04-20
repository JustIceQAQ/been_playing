import asyncio
import base64
import json
import secrets

import bs4
import httpx

from app.exhibition.tmc.parse import TmcParse
from helpers.cache.none import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class TmcRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TmcParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="台北流行音樂中心",
            code_name="Tmc",
            external_link="https://www.tmc.taipei/tw/lastest-event",
        )

    def create_filter_base64_string(self, page_number: int) -> str:
        str_dict = json.dumps(
            {
                "pages": page_number,
                "category": "",
                "year": "",
                "month": "",
                "keyword": "",
            }
        )
        return base64.b64encode(str_dict.encode()).decode()

    async def fetch_response(self):
        headers = {
            **get_header(),
            "accept": "text/html,"
            "application/xhtml+xml,"
            "application/xml;q=0.9,"
            "image/avif,"
            "image/webp,"
            "image/apng,*/*;q=0.8,"
            "application/signed-exchange;v=b3;q=0.7",
            "Host": "www.tmc.taipei",
        }
        cookie_jar = httpx.Cookies()
        cookie_jar.set("ci_session", secrets.token_hex(8), domain="www.tmc.taipei")
        target_url = "https://www.tmc.taipei/tw/lastest-event"
        url_1 = f"{target_url}?filter={self.create_filter_base64_string(1)}"
        responses_text = []
        async with HttpxAsyncClient(headers=headers, cookies=cookie_jar) as client:
            response = await client.get(url_1)
            responses_text.append(response.text)
            pagination_len = (
                len(
                    self.translation()
                    .translation_to_object(response.text)
                    .select("li.c-pagination-item")
                )
                - 2
            )
            if pagination_len != 1:
                for n in range(2, pagination_len + 1):
                    sub_url = (
                        f"{target_url}?filter={self.create_filter_base64_string(n)}"
                    )
                    sub_response = await client.get(sub_url)
                    responses_text.append(sub_response.text)

        return responses_text

    async def fetch_parsed(self):
        items = []
        parsers: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        for parsed in parsers:
            items.extend(
                parsed.select(".card-section > div.card-wrap > a.c-card-clip-wrap")
            )
        return items


async def main():
    await TmcRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
