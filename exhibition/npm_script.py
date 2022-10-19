from pathlib import Path
from typing import Dict

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import NpmColParse, NpmRowParse
from helper.runner_helper import RunnerInit


class NPMRunner(RunnerInit):
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1"
    use_method = "GET"
    target_domain = "https://www.npm.gov.tw/"
    target_storage = str(root_dir / "data" / "npm_exhibition.json")
    target_systematics = ExhibitionEnum.npm
    target_visit_url = "https://www.npm.gov.tw/Articles.aspx?sno=02007001"
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = None
    use_parse = {"row": NpmRowParse, "col": NpmColParse}

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(self.use_method, headers=headers)

    def get_items(self, response) -> Dict:
        datasets_row = response.select("ul.mt-4 li.mb-8")
        datasets_col = response.select("ul.mt-10 li.mb-8")
        return {"row": datasets_row, "col": datasets_col}

    def get_parsed(self, items: Dict):
        datasets_row = items.get("row")
        datasets_col = items.get("col")

        for item in datasets_row:
            npm_row_data = self.use_parse.get("row")(item).parsed(
                target_domain=self.target_domain,
                used_this_to_clean=RequestsClean.clean_string,
            )
            npm_row_clean_data = {
                key: RequestsClean.clean_string(value)
                for key, value in npm_row_data.items()
            }
            exhibition = self.exhibition_model(
                systematics=self.target_systematics, **npm_row_clean_data
            )
            yield exhibition
        for item in datasets_col:
            npm_col_data = self.use_parse.get("col")(item).parsed(
                target_domain=self.target_domain,
                used_this_to_clean=RequestsClean.clean_string,
            )
            npm_col_clean_data = {
                key: RequestsClean.clean_string(value)
                for key, value in npm_col_data.items()
            }
            exhibition = self.exhibition_model(
                systematics=self.target_systematics, **npm_col_clean_data
            )
            yield exhibition

    def get_visit(self, *args, **kwargs):
        requests_worker = self.instantiation(self.target_visit_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.fetch(self.use_method, headers=headers)
        opening = response.select_one("div.visit-content > p")
        visit_info = "\n".join(
            [
                info_string
                for info in response.select(
                    "ul.visit-list > li:nth-child(1) > div.visit-content > ul > li > small"
                )
                if (info_string := info.get_text())
            ]
        )
        return opening.get_text() + "\n" + visit_info


if __name__ == "__main__":
    NPMRunner().run(use_pickled=False)
