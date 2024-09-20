import base64
import json
import secrets
from pathlib import Path

import requests

from exhibition import ExhibitionEnum
from exhibition.tmc.header import TMCHeader
from exhibition.tmc.parse import TMCParse
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.runner_helper import RunnerInit


class TMCRunner(RunnerInit):
    """台北流行音樂中心"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = "https://www.tmc.taipei/tw/lastest-event"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "tmc_exhibition.json")
    target_systematics = ExhibitionEnum.TMC
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = TMCHeader
    use_parse = TMCParse

    def create_filter_base64_string(self, page_number: int) -> str:

        str_dict = json.dumps({"pages": page_number, "category": "", "year": "", "month": "", "keyword": ""})

        return (
            base64.b64encode(
                str_dict.encode()
            )
            .decode()
        )

    def get_response(self):

        s = requests.session()
        s.cookies.set("ci_session", secrets.token_hex(8), domain="www.tmc.taipei")

        items = []
        url_1 = f"{self.target_url}?filter={self.create_filter_base64_string(1)}"
        requests_worker = self.instantiation(url_1)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.fetch(self.use_method, headers=headers, cookies=s.cookies)
        items.extend(response.select(".card-section > div.card-wrap > a.c-card-clip-wrap"))

        pagination_len = len(response.select("li.c-pagination-item")) - 2
        if pagination_len == 1:
            pass
        else:
            for n in range(2, pagination_len + 1):
                url = f"{self.target_url}?filter={self.create_filter_base64_string(n)}"
                requests_worker2 = RequestsBeautifulSoupInstantiation(
                    url
                )
                response = requests_worker2.fetch(self.use_method, headers=headers, cookies=s.cookies)
                items.extend(response.select(".card-section > div.card-wrap > a.c-card-clip-wrap"))
        return items

    def get_items(self, response):
        return response

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
    TMCRunner().run(use_pickled=False)
