import asyncio
import copy
import json
import re
import urllib.parse

import bs4
from rnet import Proxy

from app.platform.kkday.parse import KKDayParse
from app.platform.kkday.utils import parse_list
from configs.settings import get_settings
from helpers.cache import NoneCache
from helpers.crawler.rnet.helper import RNetAsyncClient
from helpers.headers_helper import get_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3, date_format_digit


class KKDayRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KKDayParse
    target_url = "https://www.kkday.com/zh-tw/product/productlist"
    query_parameter = {
        "destination": ["D-TW-5013", "D-TW-4736"],
        "product_categories": [
            "CATEGORY_016",
        ],
        "currency": "TWD",
        "count": 10,
        "page": 1,
        "sort": "prec",
        "sale_date_from": date_format_digit()
    }

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="KKDay",
            code_name="KKDay",
            external_link="https://www.kkday.com/zh-tw/product/productlist?"
                          "destination=D-TW-5013,D-TW-4736&"
                          "product_categories=CATEGORY_016&"
                          "currency=TWD&"
                          "sort=prec&"
                          "page=1&"
                          "start=10&"
                          "count=10",
        )

    def _get_this_url(self, page: int | None = 1):
        runtime_query_parameter = copy.deepcopy(KKDayRunner.query_parameter)
        runtime_query_parameter["page"] = page
        parse_list_result = parse_list(runtime_query_parameter)
        encoded_query_parameter = urllib.parse.urlencode(parse_list_result, safe=',')
        return f"{self.target_url}?{encoded_query_parameter}"

    def _format_init_state(
            self, transitioned: bs4.BeautifulSoup
    ) -> tuple[list[dict], int | None]:
        products = []
        product_count = None
        script_content = transitioned.find_all(
            "script", string=re.compile(r"window\.__INIT_STATE__\s*=\s*")
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
        headers = get_headers(
            not_use_user_agent=True,
            host="www.kkday.com",
            referer="https://www.kkday.com/zh-tw/product/productlist?product_categories=CATEGORY_016&currency=TWD&start=0&count=10&sort=prec&page=2&destination=D-TW-5013,D-TW-4736",
            other_headers={
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            }
        )
        runtime_settings = get_settings()
        proxies = (
            None
            if runtime_settings.PROXY_POOL is None
            else [
                Proxy.all(
                    runtime_settings.PROXY_POOL
                )
            ]
        )
        async with RNetAsyncClient(
                proxies=proxies,
        ) as client:
            first_response = await client.get(self._get_this_url(), headers=headers)

            if (not first_response.status_code.is_success()):
                return []
            first_context = await first_response.text()
            responses.append(first_context)
            _, product_count = self._format_init_state(
                self.translation().translation_to_object(
                    first_context, format_encoding="html.parser"
                )
            )
            if product_count is not None:
                loop_number = (product_count // 10) + 2
                sub_tasks = [
                    client.get(self._get_this_url(i), headers=headers)
                    for i in range(2, loop_number, 1)
                ]
                sub_responses = await asyncio.gather(*sub_tasks)
                for sub_response in sub_responses:
                    sub_context = await sub_response.text()
                    if sub_response.status_code.is_success():
                        responses.append(sub_context)
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
