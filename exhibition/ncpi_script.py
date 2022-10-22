from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.header_helper import NCPIHeader, NCPIVisitHeader
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import NCPIParse
from helper.runner_helper import RunnerInit


class NCPIRunner(RunnerInit):
    """國家攝影文化中心"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://ncpiexhibition.ntmofa.gov.tw/tw/Exhibition/ListCur"
    use_method = "GET"
    target_domain = "https://ncpiexhibition.ntmofa.gov.tw/"
    target_storage = str(root_dir / "data" / "ncpi_exhibition.json")
    target_systematics = ExhibitionEnum.NCPI
    target_visit_url = "https://ncpi.ntmofa.gov.tw/visit.html"
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = NCPIHeader
    use_visit_header = NCPIVisitHeader
    use_parse = NCPIParse

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(self.use_method, headers=headers)

    def get_items(self, response):
        return response.select("a.exhibition_list")

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
            self.use_visit_header().get_header()
            if self.use_visit_header is not None
            else None
        )
        response = requests_worker.fetch(self.use_method, headers=headers)
        opening_info = response.select(
            "#Visit > div.primary-info > div > div.info-box > div.work-time"
        )

        opening = "\n".join(
            [
                f'{info.select_one(".title").get_text()}: {info.select_one(".time").get_text()}'
                for info in opening_info
            ]
        )
        return opening


if __name__ == "__main__":
    NCPIRunner().run(use_pickled=False)
