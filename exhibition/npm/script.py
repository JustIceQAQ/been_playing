import os
from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.npm.parse import NpmColParse, NpmRowParse
from helper.clean_helper import RequestsClean
from helper.crawler.scrape_do import ScrapeDoCrawler
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.runner_helper import RunnerInit
from helper.translation_helper import BeautifulSoupTranslation


class NPMRunner(RunnerInit):
    """國立故宮博物院"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = (
        "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1&type=1"
    )
    use_method = "GET"
    target_domain = "https://www.npm.gov.tw/"
    target_storage = str(root_dir / "data" / "npm_exhibition.json")
    target_systematics = ExhibitionEnum.NPM
    target_visit_url = "https://www.npm.gov.tw/Articles.aspx?sno=02007001"
    instantiation = RequestsBeautifulSoupInstantiation
    use_crawler = ScrapeDoCrawler
    use_translation = BeautifulSoupTranslation
    use_header = None
    use_parse = {"row": NpmRowParse, "col": NpmColParse}

    def get_response(self):
        crawler = self.use_crawler(token=os.getenv("SCRAPE_DO_API_KEY", None))
        context = crawler.get_page(self.target_url)
        return self.use_translation().format_to_object(context)

    def get_items(self, response) -> dict:
        datasets_row = response.select("ul.mt-4 li.mb-8")
        datasets_col = response.select("ul.mt-10 li.mb-8")
        return {"row": datasets_row, "col": datasets_col}

    def get_parsed(self, items: dict):
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
        crawler = self.use_crawler(token=os.getenv("SCRAPE_DO_API_KEY", None))
        context = crawler.get_page(self.target_visit_url)
        response = self.use_translation().format_to_object(context)
        opening = response.select_one("div.visit-content > p")

        if opening is None:
            return None

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
