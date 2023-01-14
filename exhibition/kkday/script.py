import os
from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.kkday.header import KKDayHeader
from exhibition.kkday.parse import KKDayParse
from helper.clean_helper import RequestsClean
from helper.crawler_helper import ScraperAsyncApiCrawler
from helper.runner_helper import RunnerInit


class KKDayRunner(RunnerInit):
    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = (
        "https://www.kkday.com/zh-tw/product/ajax_productlist/A01-001?"
        "city=&"
        "row=50&"
        "glang=&"
        "cat=TAG_3&"
        "availstartdate=&"
        "availenddate=&"
        "fprice=&"
        "eprice=&"
        "sort=prec&"
        "page=1"
    )
    use_method = "GET"
    target_storage = str(root_dir / "data" / "kkday_exhibition.json")
    target_systematics = ExhibitionEnum.KKDay
    use_crawler = ScraperAsyncApiCrawler
    use_header = KKDayHeader
    use_parse = KKDayParse

    def get_response(self):
        requests_worker = self.use_crawler(api_key=os.getenv("SCRAPER_API_KEY", None))
        return requests_worker.get_page(self.target_url).get_response(sleep_secs=60)

    def get_items(self, response):
        return response.get("data")

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


if __name__ == "__main__":
    KKDayRunner().run(use_pickled=False)
