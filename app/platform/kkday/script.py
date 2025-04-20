import asyncio
import http
import json
import re
import urllib.parse

import bs4

from app.platform.kkday.parse import KKDayParse
from app.platform.kkday.utils import parse_list
from configs.settings import get_settings
from helpers.cache import NoneCache
from helpers.crawler.scraper.helper import ScraperAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class KKDayRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KKDayParse
    target_url = "https://www.kkday.com/zh-tw/product/productlist"
    query_parameter = {
        "city": ["A01-001-00001", "A01-001-00006"],
        "prodcat": [
            "CATEGORY_016",
        ],
        "currency": "TWD",
        "start": 0,
        "count": 10,
        "sort": "prec",
    }

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="KKDay",
            code_name="KKDay",
            external_link="https://www.kkday.com/zh-tw/country/taiwan/events-and-exhibitions?sort=prec&page=1",
        )

    def _get_this_url(self, page: int | None = 1):
        parse_list_result = parse_list(KKDayRunner.query_parameter)
        encoded_query_parameter = urllib.parse.urlencode(parse_list_result)
        encoded_query_parameter += f"&page={page}"
        return f"{self.target_url}?{encoded_query_parameter}"

    def _format_init_state(
        self, transitioned: bs4.BeautifulSoup
    ) -> tuple[list[dict], int | None]:
        products = []
        product_count = None
        script_content = transitioned.find_all(
            "script", text=re.compile(r"window\.__INIT_STATE__\s*=\s*")
        )
        for script in script_content:
            match = re.search(
                r"window\.__INIT_STATE__\s*=\s*(\{.*?\})\s*;", script.string, re.DOTALL
            )
            if match:
                init_state_json = match.group(1)
                raw_data = json.loads(init_state_json)
                state = raw_data["state"]
                if (state.get("products", None) is None) or (
                    state.get("productCount", None) is None
                ):
                    continue
                products = raw_data["state"]["products"]
                product_count = raw_data["state"]["productCount"]
                break
        return products, product_count

    async def fetch_response(self):
        responses = []
        runtime_settings = get_settings()
        headers = {
            **get_header(),
            "host": "www.kkday.com",
            "Referer": "https://www.kkday.com/zh-tw/country/taiwan/events-and-exhibitions?cat=TAG_3&sort=prec&page=1",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        async with ScraperAsyncClient(
            api_key=runtime_settings.SCRAPER_API_KEY
        ) as client:
            first_response = await client.get(self._get_this_url(), headers=headers)
            if first_response.status_code != http.HTTPStatus.OK:
                return []
            responses.append(first_response.response.body)
            _, product_count = self._format_init_state(
                self.translation().translation_to_object(
                    first_response.response.body, format_encoding="html.parser"
                )
            )
            if product_count is not None:
                loop_number = (product_count // 10) + 2
                sub_tasks = [
                    client.get(self._get_this_url(i), sleep_secs=10)
                    for i in range(2, loop_number, 1)
                ]
                sub_responses = await asyncio.gather(*sub_tasks)
                for sub_response in sub_responses:
                    if sub_response.status_code == http.HTTPStatus.OK:
                        responses.append(sub_response.response.body)
            return responses

    async def fetch_parsed(self):
        dataset = []
        parsers: list[bs4.BeautifulSoup] = await super().fetch_parsed(
            format_encoding="html.parser"
        )
        for parsed in parsers:
            products, _ = self._format_init_state(parsed)
            dataset.extend(products)
        return dataset


async def main():
    await KKDayRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
