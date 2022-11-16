from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.header_helper import NMHHeader
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import NMHParse
from helper.runner_helper import RunnerInit


class NMHRunner(RunnerInit):
    """國立歷史博物館"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.nmh.gov.tw/activitysoonlist_66.html"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "nmh_exhibition.json")
    target_systematics = ExhibitionEnum.NMH
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = NMHHeader
    use_parse = NMHParse
    target_visit_url = "https://www.nmh.gov.tw/qa_146_3275_1.html"

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(self.use_method, headers=headers)

    def get_items(self, response):
        return response.select("ul.lists > li.item")

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

    def get_visit(self, *args, **kwargs):
        requests_worker = self.instantiation(self.target_visit_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.fetch(self.use_method, headers=headers)
        opening = response.select_one("li.qa-item:nth-child(1) > div > div > p")

        return None if opening is None else opening.get_text()


if __name__ == "__main__":
    NMHRunner().run(use_pickled=False)
