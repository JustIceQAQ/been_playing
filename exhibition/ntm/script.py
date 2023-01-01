from itertools import chain, product
from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.ntm.parse import NTMParse
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.runner_helper import RunnerInit


class NTMRunner(RunnerInit):
    """國立臺灣博物館"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_domain = "https://www.ntm.gov.tw"
    urls_format = "{}/exhibitionlist_{}.html?Type={}"
    target_visit_url = "https://www.ntm.gov.tw/content_158.html"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "ntm_exhibition.json")
    target_systematics = ExhibitionEnum.NTM
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = None
    use_parse = NTMParse

    def get_response(self):
        product_data = product(
            (
                "179",
                "182",
                "185",
                "383",
                "380",
            ),
            (
                "PE1",
                "SP1",
            ),
        )
        target_urls = list(
            self.urls_format.format(self.target_domain, *item) for item in product_data
        )

        requests_workers = list(
            self.instantiation(target_url) for target_url in target_urls
        )
        target_objects = list(
            requests_worker.fetch() for requests_worker in requests_workers
        )
        return target_objects

    def get_items(self, responses):
        return list(
            chain.from_iterable(
                response.select("#exhibition-list > dl") for response in responses
            )
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

    def get_visit(self, *args, **kwargs):
        requests_worker = self.instantiation(self.target_visit_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.fetch(self.use_method, headers=headers)
        opening = response.select_one("#visit > .info > p")
        return opening.get_text().replace("＊", "\n＊")


if __name__ == "__main__":
    NTMRunner().run(use_pickled=False)
