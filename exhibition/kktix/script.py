from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.kktix.header import KKTixHeader
from exhibition.kktix.parse import KKTixParse
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.runner_helper import RunnerInit


class KKTixRunner(RunnerInit):
    """KKTix"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = "https://kktix.com/events?category_id=11"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "kktix_exhibition.json")
    target_systematics = ExhibitionEnum.KKTix
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = KKTixHeader
    use_parse = KKTixParse

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(self.use_method, headers=headers)

    def get_items(self, response):
        return response.select("ul.events > li.type-selling") + response.select("ul.events > li.type-view")

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
        return None


if __name__ == "__main__":
    KKTixRunner().run(use_pickled=False)
