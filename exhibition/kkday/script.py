import os
from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.kkday.header import KKDayHeader
from exhibition.kkday.parse import KKDayParse
from helper.clean_helper import RequestsClean
from helper.crawler_helper import ScraperAsyncApiCrawler
from helper.runner_helper import RunnerInit
from helper.translation_helper import JsonTranslation


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
    use_translation = JsonTranslation
    use_header = KKDayHeader
    use_parse = KKDayParse

    def get_response(self):
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        pre_tasks = self.use_crawler(
            api_key=os.getenv("SCRAPER_API_KEY", None)
        ).get_page(
            self.target_url,
            headers=headers,
            render=True,
        )
        pre_tasks_runtime_result = pre_tasks.get_status()

        print(pre_tasks_runtime_result)

        return pre_tasks_runtime_result[1]

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
    os.environ["SCRAPER_API_KEY"] = "28142a7fa0077c2e3ad1d5d9680b3c81"

    KKDayRunner().run(use_pickled=False)
