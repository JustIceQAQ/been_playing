from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import NTSECParse
from helper.runner_helper import RunnerInit


class NTSECRunner(RunnerInit):
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.ntsec.gov.tw/User/Exhibitions.aspx?a=44"
    use_method = "GET"
    target_domain = "https://www.ntsec.gov.tw"
    target_storage = str(root_dir / "data" / "ntsec_exhibition.json")
    target_systematics = ExhibitionEnum.ntsec
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = None
    use_parse = NTSECParse

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(self.use_method, headers=headers)

    def get_items(self, response):
        return response.select("#ctl00_artContent > ul > li")

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
        pass


if __name__ == "__main__":
    # ntsec_script(use_pickled=False)
    NTSECRunner().run(use_pickled=False)
