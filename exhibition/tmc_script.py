from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import TMCParse
from helper.runner_helper import RunnerInit


class TMCRunner(RunnerInit):
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://tmc.taipei/show/event/"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "tmc_exhibition.json")
    target_systematics = ExhibitionEnum.tmc
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = None
    use_parse = TMCParse

    def get_response(self):
        items = []
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.fetch(self.use_method, headers=headers)
        items.extend(response.select(".o-archive-frame__cards > div"))

        pagination__list = response.select(".m-pagination__list > div > a")
        pagination = {
            this_pagination
            for pagination in pagination__list
            if (this_pagination := pagination.get("href", ""))
        }
        for pagination_url in pagination:
            requests_worker = self.instantiation(pagination_url)
            dataset = requests_worker.fetch()
            items.extend(dataset.select(".o-archive-frame__cards > div"))
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
