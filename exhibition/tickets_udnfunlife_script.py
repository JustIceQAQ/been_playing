import json
from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.header_helper import TicketsUdnFunLifeHeader
from helper.instantiation_helper import RequestsJsonInstantiation
from helper.parse_helper import TicketsUdnFunLifeParse
from helper.runner_helper import RunnerInit
from helper.translation_helper import BeautifulSoupTranslation


class TicketsUdnFunLifeRunner(RunnerInit):
    """udn售票網"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = (
        "https://tickets.udnfunlife.com/application/UTK01/UTK0101_.aspx/GET_PUSH_LIST"
    )
    target_storage = str(root_dir / "data" / "udnfunlife_exhibition.json")
    target_systematics = ExhibitionEnum.TicketsUdnFunLife
    instantiation = RequestsJsonInstantiation
    use_header = TicketsUdnFunLifeHeader
    use_parse = TicketsUdnFunLifeParse

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(
            method="POST",
            headers=headers,
            data=json.dumps({"pageNo": "1", "pageSize": "100"}),
        )

    def get_items(self, response):
        rawdata = BeautifulSoupTranslation().format_to_object(
            response["d"]["ReturnData"]["script"]
        )
        return rawdata.select("div.inner")

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
    TicketsUdnFunLifeRunner().run(use_pickled=False)
