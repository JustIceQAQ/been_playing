from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import HuaShan1914Parse
from helper.runner_helper import RunnerInit


class HuaShan1914Runner(RunnerInit):
    """華山1914文化創意產業園區"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.huashan1914.com/w/huashan1914/exhibition"
    target_domain = "https://www.huashan1914.com"
    target_storage = str(root_dir / "data" / "huashan1914_exhibition.json")
    target_systematics = ExhibitionEnum.HuaShan1914
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = None
    use_parse = HuaShan1914Parse

    def get_response(self):
        index = 1
        datasets = []
        while True:
            requests_worker = self.instantiation(f"{self.target_url}?index={index}")
            target_object = requests_worker.fetch()
            dataset = target_object.select("ul#event-ul li")
            if dataset:
                datasets.extend(dataset)
                index = index + 1
            else:
                break
        return datasets

    def get_items(self, response):
        return response

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


if __name__ == "__main__":
    HuaShan1914Runner().run(use_pickled=False)
