import os
import time
from pathlib import Path
from typing import List

from exhibition import ExhibitionEnum
from exhibition.klook.parse import KLookParse
from helper.clean_helper import RequestsClean
from helper.crawler.scraper import ScraperAsyncApiCrawler
from helper.runner_helper import RunnerInit
from helper.translation_helper import BeautifulSoupTranslation


class KLookRunner(RunnerInit):
    """KLOOK客路"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = "https://www.klook.com/zh-TW/event/city-mcate/19-3-taipei-convention-exhibition-tickets/"
    target_domain = "https://www.klook.com/"
    target_storage = str(root_dir / "data" / "klook_exhibition.json")
    target_systematics = ExhibitionEnum.KLook
    use_crawler = ScraperAsyncApiCrawler
    use_translation = BeautifulSoupTranslation
    use_parse = KLookParse
    use_header = None
    while_sleep = 20

    def get_response(self):
        dataset_list = []
        headers = {
            "referer": "https://www.klook.com/zh-TW/event/19-taipei/",
        }
        pre_tasks = self.use_crawler(
            api_key=os.getenv("SCRAPER_API_KEY", None)
        ).get_page(self.target_url, headers=headers)

        pagination = self.get_first_page(dataset_list, pre_tasks)

        tasks: List[ScraperAsyncApiCrawler] = []
        for runtime_url, referer_url in zip(pagination[1:], pagination):
            tasks.append(
                self.use_crawler(api_key=os.getenv("SCRAPER_API_KEY", None)).get_page(
                    runtime_url,
                    render=True,
                    headers={
                        "referer": referer_url,
                    },
                )
            )

        return self.get_pagination_page(dataset_list, tasks)

    def get_pagination_page(
            self, dataset_list: List, tasks: List[ScraperAsyncApiCrawler]
    ):
        while True:
            runtime_tasks = [job.get_status() for job in tasks]
            if all([n.status for n in runtime_tasks]):
                for runtime_data in runtime_tasks:
                    dataset_list.append(
                        self.use_translation().format_to_object(runtime_data.response)
                    )
                break
            else:
                time.sleep(self.while_sleep)
        return dataset_list

    def get_first_page(self, dataset_list: List, pre_tasks: ScraperAsyncApiCrawler):
        while True:
            pre_tasks_runtime_result = pre_tasks.get_status()
            if pre_tasks_runtime_result.status:
                pre_tasks_body = self.use_translation().format_to_object(
                    pre_tasks_runtime_result.response
                )
                dataset_list.append(pre_tasks_body)
                pagination = [
                    f'{self.target_domain}{a.get("href")}'
                    for a in pre_tasks_body.select("div.klk-pagination > ul > li > a")
                ]
                break
            else:
                time.sleep(self.while_sleep)
        return pagination

    def get_items(self, response):
        items = []
        for r in response:
            layout_list = r.select("a.layout_list")
            items.extend(layout_list)

        return items

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
