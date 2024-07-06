import json
import os
import re
from pathlib import Path
import urllib.parse
from typing import Tuple, Optional

from bs4 import BeautifulSoup

from exhibition import ExhibitionEnum
from exhibition.kkday.header import KKDayHeader
from exhibition.kkday.parse import KKDayParse
from helper.clean_helper import RequestsClean
from helper.crawler.scraper import ScraperAsyncApiCrawler
from helper.runner_helper import RunnerInit


class KKDayRunner(RunnerInit):
    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = "https://www.kkday.com/zh-tw/product/productlist"
    query_parameter = {
        "city": ["A01-001-00001", "A01-001-00006"],
        "prodcat": [
            "CATEGORY_016",
            "CATEGORY_004",
            "CATEGORY_011",
        ],
        "currency": "TWD",
        "start": 0,
        "count": 10,
        "sort": "prec"
    }
    use_method = "GET"
    target_storage = str(root_dir / "data" / "kkday_exhibition.json")
    target_systematics = ExhibitionEnum.KKDay
    use_crawler = ScraperAsyncApiCrawler
    use_header = KKDayHeader
    use_parse = KKDayParse

    def get_this_url(self, page: int | None = 1):
        parse_list_result = parse_list(KKDayRunner.query_parameter)
        encoded_query_parameter = urllib.parse.urlencode(parse_list_result)
        encoded_query_parameter += f"&page={page}"
        return f"{self.target_url}?{encoded_query_parameter}"

    def format_init_state(self, response: str) -> Tuple[list[dict], Optional[int]]:
        products = []
        product_count = None
        soup = BeautifulSoup(response, "html.parser")
        script_content = soup.find_all('script', text=re.compile(r'window\.__INIT_STATE__\s*=\s*'))
        for script in script_content:
            match = re.search(r'window\.__INIT_STATE__\s*=\s*(\{.*?\})\s*;', script.string, re.DOTALL)
            if match:
                init_state_json = match.group(1)
                raw_data = json.loads(init_state_json)
                products = raw_data["state"]["products"]
                product_count = raw_data["state"]["productCount"]
                break
        return products, product_count

    def get_response(self):
        requests_worker = self.use_crawler(api_key=os.getenv("SCRAPER_API_KEY", None))
        this_url = self.get_this_url()
        responses = []
        first_response = requests_worker.get_page(this_url).get_response(sleep_secs=10)
        responses.append(first_response)

        _, product_count = self.format_init_state(first_response)
        if product_count is not None:
            loop_number = (product_count // 10) + (product_count % 10)+1
            for i in range(2, loop_number, 1):
                this_url = self.get_this_url(i)
                other_response = requests_worker.get_page(this_url).get_response(sleep_secs=10)
                responses.append(other_response)

        return responses

    def get_items(self, responses: list[str]):
        dataset = []
        for response in responses:
            products, _ = self.format_init_state(response)
            dataset.extend(products)

        return dataset

    def get_parsed(self, items):
        for item in items:
            data = self.use_parse(item).parsed()
            clean_data = {
                key: RequestsClean.clean_string(value) for key, value in data.items()
            }
            exhibition = self.exhibition_model(
                systematics=self.target_systematics, **clean_data
            )
            yield exhibition


def parse_list(data: dict) -> dict:
    result = {}
    for key, value in data.items():
        if isinstance(value, list):
            result[key] = ",".join(value)
        else:
            result[key] = value
    return result


if __name__ == "__main__":
    KKDayRunner().run(use_pickled=False)
