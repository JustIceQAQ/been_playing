from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.fubonartmuseum.header import FuBonArtMuseumHeader
from exhibition.fubonartmuseum.parse import FuBonArtMuseumParse
from helper.clean_helper import RequestsClean
from helper.crawler.requests_ import RequestsCrawler
from helper.proxy_helper import NoneProxy
from helper.runner_helper import RunnerInit
from helper.translation_helper import BeautifulSoupTranslation


class FuBonArtMuseumRunner(RunnerInit):
    """富邦博物館"""

    use_method = "GET"
    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = "https://www.fubonartmuseum.org/Default"
    target_storage = str(root_dir / "data" / "fubonartmuseum_exhibition.json")
    target_systematics = ExhibitionEnum.FuBonArtMuseum
    use_crawler = RequestsCrawler
    use_translation = BeautifulSoupTranslation
    use_parse = FuBonArtMuseumParse
    use_header = FuBonArtMuseumHeader
    use_proxy = NoneProxy

    def get_response(self):
        requests_worker = self.use_crawler(self.target_url, module_proxy=self.use_proxy)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.get_page(
            self.use_method, headers=headers, formatted=requests_worker.Formatted.text
        )
        transitioned = self.use_translation().format_to_object(response)
        return transitioned

    def get_items(self, response):
        return response.select(
            "div#homepage-swiper-exhibitions > div.swiper-wrapper > div"
        )

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
    FuBonArtMuseumRunner().run(use_pickled=False)
