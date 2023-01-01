from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.mwr.header import MWRHeader
from exhibition.mwr.parse import MWRParse
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.runner_helper import RunnerInit


class MWRRunner(RunnerInit):
    """世界宗教博物館"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent
    xsmsid = "0H305741810776620070"
    target_url = f"https://www.mwr.org.tw/xcspecexhi?xsmsid={xsmsid}"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "mwr_exhibition.json")
    target_systematics = ExhibitionEnum.MWR
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = MWRHeader
    use_parse = MWRParse
    target_visit_url = "https://www.mwr.org.tw/xmdoc/cont?xsmsid=0H305737466544602901"

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(self.use_method, headers=headers)

    def get_items(self, response):
        return response.select("div.ce_list > div.item")

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
        opening = response.select_one(
            "#MainForm > div.editable_content.content.dev-xew-block > div:nth-child(1) > p:nth-child(4)"
        )
        return opening.get_text().replace("\u3000", "")


if __name__ == "__main__":
    MWRRunner().run(use_pickled=False)
