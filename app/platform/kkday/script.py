import asyncio
import copy
import json
import re
import urllib.parse
from typing import cast, TypedDict

import bs4
from wreq import Proxy

from app.platform.kkday.parse import KKDayParse
from app.platform.kkday.utils import parse_list
from configs.settings import get_settings
from helpers.crawler.wreq.helper import WReqAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3, get_date


class KKDayQueryParameter(TypedDict):
    destination: list[str]
    product_categories: list[str]
    currency: str
    count: int
    page: int
    sort: str
    sale_date_from: str


class KKDayRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KKDayParse
    target_url = "https://www.kkday.com/zh-tw/product/productlist"
    query_parameter: KKDayQueryParameter = {
        "destination": [
            "D-TW-5013",
            "D-TW-4740",
            "D-TW-4742",
            "D-TW-4739",
            "D-TW-4736",
            "D-TW-4730",
            "D-TW-4738",
            "D-TW-4743",
            "D-TW-4727",
            "D-TW-4735",
            "D-TW-4728",
            "D-TW-4731",
            "D-TW-4726",
            "D-TW-4729",
            "D-TW-4737",
            "D-TW-4734",
            "D-TW-4744",
            "D-TW-4741",
            "D-TW-4732",
            "D-TW-4733",
        ],
        "product_categories": [
            "CATEGORY_016",
        ],
        "currency": "TWD",
        "count": 10,
        "page": 1,
        "sort": "prec",
        "sale_date_from": get_date.now_format_to_digit,
    }

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        destination = ",".join(self.query_parameter.get("destination"))
        product_categories = self.query_parameter.get("product_categories")
        return Information(
            fullname="KKDay",
            code_name="KKDay",
            external_link="https://www.kkday.com/zh-tw/product/productlist?"
            f"destination={destination}&"
            f"product_categories={product_categories}&"
            "currency=TWD&"
            "sort=prec&"
            "page=1&"
            "start=10&"
            "count=10",
            venue_type=VenueType.PLATFORM,
        )

    def _get_this_url(self, page: int = 1):
        runtime_query_parameter = copy.deepcopy(KKDayRunner.query_parameter)
        runtime_query_parameter["page"] = page
        parse_list_result = parse_list(runtime_query_parameter)
        encoded_query_parameter = urllib.parse.urlencode(parse_list_result, safe=",")
        return f"{self.target_url}?{encoded_query_parameter}"

    def _format_init_state(self, transitioned: bs4.BeautifulSoup) -> tuple[list[dict], int | None]:
        products = []
        product_count = None
        script_content = transitioned.find_all("script", string=re.compile(r"window\.__INIT_STATE__\s*=\s*"))
        for script in script_content:
            match = re.search(r"window\.__INIT_STATE__\s*=\s*(\{.*?\})\s*;", script.string, re.DOTALL)
            if match:
                init_state_json = match.group(1)
                raw_data = json.loads(init_state_json)
                state = raw_data["state"]
                if (state.get("products", None) is None) or (state.get("productCount", None) is None):
                    continue
                products = raw_data["state"]["products"]
                product_count = raw_data["state"]["productCount"]
                break
        return products, product_count

    def _has_sold_out_divider(self, soup: bs4.BeautifulSoup) -> bool:
        span = soup.find("span", class_="kk-divider__text kk-divider__text--body-md")
        return span is not None and "暫時已售罄" in span.get_text()

    def _count_products_before_divider(self, soup: bs4.BeautifulSoup) -> int | None:
        span = soup.find("span", class_="kk-divider__text kk-divider__text--body-md")
        if span is None:
            return None
        node = span
        while node.parent:
            node = node.parent
            prev_siblings = [s for s in node.previous_siblings if getattr(s, "name", None) is not None]
            if prev_siblings:
                return len(prev_siblings)
        return None

    async def fetch_response(self):
        responses = []
        headers = generate_headers(
            not_use_user_agent=True,
            host="www.kkday.com",
            referer="https://www.kkday.com/zh-tw/product/productlist?product_categories=CATEGORY_016&currency=TWD&start=0&count=10&sort=prec&page=2&destination=D-TW-5013,D-TW-4736",
            other_headers={
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            },
        )
        runtime_settings = get_settings()
        proxies = None if runtime_settings.PROXY_POOL is None else [Proxy.all(runtime_settings.PROXY_POOL)]
        async with WReqAsyncClient(
            proxies=proxies,
        ) as client:
            first_response = await client.get(self._get_this_url(), headers=headers)
            if not first_response.status.is_success():
                return []
            first_context = await first_response.text()
            responses.append(first_context)
            first_soup = self.translation().translation_to_object(first_context, format_encoding="html.parser")
            if first_soup is None:
                return None
            if self._has_sold_out_divider(first_soup):
                return responses
            _, product_count = self._format_init_state(first_soup)
            if product_count is not None:
                loop_number = (product_count // 10) + 2
                sub_tasks = [client.get(self._get_this_url(i), headers=headers) for i in range(2, loop_number, 1)]
                sub_responses = await asyncio.gather(*sub_tasks)
                for sub_response in sub_responses:
                    sub_context = await sub_response.text()
                    if sub_response.status.is_success():
                        responses.append(sub_context)
                        sub_soup = self.translation().translation_to_object(sub_context, format_encoding="html.parser")
                        if sub_soup is None:
                            return None
                        if self._has_sold_out_divider(sub_soup):
                            break
            return responses

    async def fetch_parsed(self):
        dataset = []
        parsers = cast(list[bs4.BeautifulSoup], await super().fetch_parsed(format_encoding="html.parser"))
        for parsed in parsers:
            products, _ = self._format_init_state(parsed)
            if self._has_sold_out_divider(parsed):
                limit = self._count_products_before_divider(parsed)
                if limit is not None:
                    products = products[:limit]
            dataset.extend(products)
        return dataset


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await KKDayRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
