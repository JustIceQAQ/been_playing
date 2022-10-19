import json
from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.header_helper import TFAMLifeHeader
from helper.instantiation_helper import (
    RequestsBeautifulSoupInstantiation,
    RequestsJsonInstantiation,
)
from helper.parse_helper import TFAMParse
from helper.runner_helper import RunnerInit


class TFAMRunner(RunnerInit):
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.tfam.museum/ashx/Exhibition.ashx?ddlLang=zh-tw"
    target_storage = str(root_dir / "data" / "tfam_exhibition.json")
    target_systematics = ExhibitionEnum.tfam
    target_domain = "https://www.tfam.museum"
    target_visit_url = "https://www.tfam.museum/Common/editor.aspx?id=230&ddlLang=zh-tw"
    instantiation = RequestsJsonInstantiation
    use_header = TFAMLifeHeader
    use_parse = TFAMParse

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        dataset_1 = requests_worker.fetch(
            method="POST",
            headers=headers,
            data=json.dumps({"JJMethod": "GetEx", "Type": "1"}),
        )
        dataset_2 = requests_worker.fetch(
            method="POST",
            headers=headers,
            data=json.dumps({"JJMethod": "GetEx", "Type": "2"}),
        )
        dataset_list = []
        dataset_list.extend(dataset_1.get("Data", []))
        dataset_list.extend(dataset_2.get("Data", []))
        return dataset_list

    def get_items(self, response):
        return response

    def get_parsed(self, items):
        for item in items:
            tfam_data = self.use_parse(item).parsed(target_domain=self.target_domain)
            tfam_clean_data = {
                key: RequestsClean.clean_string(value)
                for key, value in tfam_data.items()
            }
            exhibition = self.exhibition_model(
                systematics=self.target_systematics, **tfam_clean_data
            )
            yield exhibition

    def get_visit(self, *args, **kwargs):
        requests_visit = RequestsBeautifulSoupInstantiation(self.target_visit_url)
        targe_visit_object = requests_visit.fetch()
        visit = targe_visit_object.select_one("div.spacingB-20 > .table1")
        days, openings = [th.get_text() for th in visit.select("th")], [
            td.get_text() for td in visit.select("td")
        ]
        return "\n".join([f"{day}: {opening}" for day, opening in zip(days, openings)])


if __name__ == "__main__":
    TFAMRunner().run(use_pickled=False)
