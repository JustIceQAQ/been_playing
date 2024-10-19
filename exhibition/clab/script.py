from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.clab.header import CLabHeader
from exhibition.clab.paese import CLabParse
from helper.clean_helper import RequestsClean
from helper.crawler.requests_ import RequestsCrawler
from helper.runner_helper import RunnerInit
from helper.translation_helper import BeautifulSoupTranslation
from helper.utils_helper import date_now


class CLabRunner(RunnerInit):
    """臺灣當代文化實驗場 C-LAB"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = (
        "https://clab.org.tw/events/?"
        "event_category=exhibition"
        "&filter_year={filter_year}"
        "&filter_month={filter_month}"
    )
    use_method = "GET"
    target_storage = str(root_dir / "data" / "clab_exhibition.json")
    target_systematics = ExhibitionEnum.CLab
    use_crawler = RequestsCrawler
    use_translation = BeautifulSoupTranslation
    use_header = CLabHeader
    use_parse = CLabParse

    def get_response(self):
        today = date_now()
        filter_year = today.year
        filter_month = today.month
        target_url = self.target_url.format(
            filter_year=filter_year, filter_month=filter_month
        )
        requests_worker = self.use_crawler(target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.get_page(
            self.use_method, headers=headers, formatted=requests_worker.Formatted.text
        )

        return response

    def get_items(self, response):
        return (
            self.use_translation()
            .format_to_object(response)
            .find_all("div", {"data-aos": "-block-line"})
        )

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
    CLabRunner().run(use_pickled=False)
