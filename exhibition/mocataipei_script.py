from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import MocaTaipeiParse
from helper.runner_helper import RunnerInit


class MocaTaipeiRunner(RunnerInit):
    """台北當代藝術館"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent"
    use_method = "GET"
    target_domain = "https://www.mocataipei.org.tw"
    target_storage = str(root_dir / "data" / "mocataipei_exhibition.json")
    target_systematics = ExhibitionEnum.MocaTaipei
    target_visit_url = "https://www.mocataipei.org.tw/tw/Visit/%E6%99%82%E9%96%93%E8%88%87%E7%A5%A8%E5%83%B9"
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = None
    use_parse = MocaTaipeiParse

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(self.use_method, headers=headers)

    def get_items(self, response):
        return response.select("div.listFrameBox div.list")

    def get_parsed(self, items):
        for item in items:
            data = self.use_parse(item).parsed(target_domain=self.target_domain)
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
        opening = response.select_one("section.category > .secBox > p.normal")
        return opening.get_text()


if __name__ == "__main__":
    MocaTaipeiRunner().run(use_pickled=False)
