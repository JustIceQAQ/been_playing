from itertools import chain, product
from pathlib import Path
from typing import List

from exhibition import ExhibitionEnum
from exhibition.ntm.parse import NTMParse, PathQuery
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.runner_helper import RunnerInit


class NTMRunner(RunnerInit):
    """國立臺灣博物館"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_domain = "https://www.ntm.gov.tw"
    urls_format = "{target_domain}/News_actives.aspx?n={n}&sms={sms}"
    target_visit_url = "https://www.ntm.gov.tw/content_158.html"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "ntm_exhibition.json")
    target_systematics = ExhibitionEnum.NTM
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = None
    use_parse = NTMParse

    def get_response(self):
        path_query_data: List[PathQuery] = [
            PathQuery(n=5472, sms=13389),
            PathQuery(n=5473, sms=13389),
            PathQuery(n=5474, sms=13389),
            PathQuery(n=5478, sms=13389),
            PathQuery(n=5477, sms=13389),
        ]
        target_urls = list(
            self.urls_format.format(target_domain=self.target_domain, n=item.n, sms=item.sms)
            for item in path_query_data
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
                response.select_one("#CCMS_Content").select("ul[data-child] > li[data-index] > div.area-essay")
                for response in responses
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
        return (
            ""
            if (opening_text := opening.get_text()) is None
            else opening_text.replace("＊", "\n＊")
        )


if __name__ == "__main__":
    NTMRunner().run(use_pickled=False)
