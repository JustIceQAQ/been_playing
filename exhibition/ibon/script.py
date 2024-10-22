import json
from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.ibon.header import IBonHeader
from exhibition.ibon.parse import IBonParse
from helper.clean_helper import RequestsClean
from helper.crawler.requests_ import RequestsCrawler
from helper.runner_helper import RunnerInit
from helper.translation_helper import BeautifulSoupTranslation


class IBonRunner(RunnerInit):
    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = (
        "https://tour.ibon.com.tw/api/public/event/list?"
        "page=1&"
        "limit=100&"
        "category=5fe4480d3ff56763f1bb99ba"
    )
    use_method = "GET"
    target_storage = str(root_dir / "data" / "ibon_exhibition.json")
    target_systematics = ExhibitionEnum.IBon
    use_crawler = RequestsCrawler
    use_translation = BeautifulSoupTranslation
    use_header = IBonHeader
    use_parse = IBonParse

    def get_response(self):
        requests_worker = self.use_crawler(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.get_page(
            self.use_method, headers=headers, formatted=requests_worker.Formatted.text
        )

        try:
            response_json = json.loads(response)
        except ValueError:
            response_json = {}

        return response_json

    def get_items(self, response):
        return response.get("list", [])

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
    IBonRunner().run(use_pickled=False)
