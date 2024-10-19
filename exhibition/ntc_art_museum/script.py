from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.ntc_art_museum.parse import (
    NTCArtMuseumMainParse,
    NTCArtMuseumOtherParse,
)
from helper.clean_helper import RequestsClean
from helper.crawler.requests_ import RequestsCrawler
from helper.runner_helper import RunnerInit
from helper.translation_helper import BeautifulSoupTranslation


class NTCArtMuseumRunner(RunnerInit):
    """新北市立美術館"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = "https://ntcart.museum/exhibition"
    target_domain = "https://ntcart.museum"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "ntc_art_museum_exhibition.json")
    target_systematics = ExhibitionEnum.NTCArtMuseum
    use_crawler = RequestsCrawler
    use_translation = BeautifulSoupTranslation
    use_parse = {"main": NTCArtMuseumMainParse, "other": NTCArtMuseumOtherParse}
    use_header = None

    def get_response(self):
        requests_worker = self.use_crawler(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.get_page(
            self.use_method, headers=headers, formatted=requests_worker.Formatted.text
        )
        transitioned = self.use_translation().format_to_object(response)
        return transitioned

    def get_items(self, response):
        art_content_other = response.select("div.art-content-other.ex-group > a")
        main_exhibition = response.select("div.main-pic > a")

        return {
            "art_content_other": art_content_other,
            "main_exhibition": main_exhibition,
        }

    def get_parsed(self, items: dict[str, list]):
        art_content_other = items.get("art_content_other")
        main_exhibition = items.get("main_exhibition")
        for art_content_other_item in art_content_other:
            data = self.use_parse.get("other")(art_content_other_item).parsed(
                target_domain=self.target_domain
            )
            clean_data = {
                key: RequestsClean.clean_string(value) for key, value in data.items()
            }
            exhibition = self.exhibition_model(
                systematics=self.target_systematics, **clean_data
            )
            yield exhibition
        for main_exhibition_item in main_exhibition:
            data = self.use_parse.get("main")(main_exhibition_item).parsed(
                target_domain=self.target_domain
            )
            clean_data = {
                key: RequestsClean.clean_string(value) for key, value in data.items()
            }
            exhibition = self.exhibition_model(
                systematics=self.target_systematics, **clean_data
            )
            yield exhibition


if __name__ == "__main__":
    NTCArtMuseumRunner().run(use_pickled=False)
