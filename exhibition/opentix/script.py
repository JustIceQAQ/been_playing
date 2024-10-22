from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.opentix.header import OpenTixHeader
from exhibition.opentix.parse import OpenTixParse
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsJsonInstantiation
from helper.runner_helper import RunnerInit


class OpenTixRunner(RunnerInit):
    """OPENTIX兩廳院生活文化"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = "https://search.opentix.life/search"
    target_domain = "https://www.opentix.life/event/"
    use_method = "POST"
    target_storage = str(root_dir / "data" / "opentix_exhibition.json")
    target_systematics = ExhibitionEnum.OpenTix
    instantiation = RequestsJsonInstantiation
    use_parse = OpenTixParse
    use_header = OpenTixHeader

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        dataset = requests_worker.fetch(
            method=self.use_method,
            headers=headers,
            json={
                "highlight": False,
                "language": "zh-CHT",
                "categoryFilter": ["展覽-常設展", "展覽-主題展"],
                "sortBy": "ABOUT_TO_BEGIN",
            },
        )
        return dataset.get("result", [])

    def get_items(self, response):
        return response.get("found", [])

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
    OpenTixRunner().run(use_pickled=False)
