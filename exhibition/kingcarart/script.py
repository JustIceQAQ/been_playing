from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.kingcarart.header import KingCarArtHeader
from exhibition.kingcarart.parse import KingCarArtParse
from helper.clean_helper import RequestsClean
from helper.crawler.requests_ import RequestsCrawler
from helper.runner_helper import RunnerInit
from helper.translation_helper import BeautifulSoupTranslation


class KingCarArtRunner(RunnerInit):
    """金車文藝中心"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = (
        "https://www.kingcarart.org.tw/exhibitions/current?"
        "nanjing=true"
        "&chengde=true"
        "&yuanshan=true"
        "&page={page}"
    )
    use_method = "GET"
    target_storage = str(root_dir / "data" / "kingcarart_exhibition.json")
    target_systematics = ExhibitionEnum.KingCarArt
    use_crawler = RequestsCrawler
    use_translation = BeautifulSoupTranslation
    use_header = KingCarArtHeader
    use_parse = KingCarArtParse

    def get_response(self):
        responses = []
        requests_worker = self.use_crawler(self.target_url.format(page=1))
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.get_page(
            self.use_method, headers=headers, formatted=requests_worker.Formatted.text
        )

        parsed = self.use_translation().format_to_object(response)
        responses.append(response)
        get_page_number = len(parsed.select("div.pagin-box > div.page-link"))
        for page_flag in range(2, get_page_number + 1):
            sub_response = self.use_crawler(
                self.target_url.format(page=page_flag)
            ).get_page(
                self.use_method,
                headers=headers,
                formatted=requests_worker.Formatted.text,
            )
            responses.append(sub_response)
        return responses

    def get_items(self, response: list[str]):
        items = []
        for item in response:
            items.extend(
                self.use_translation()
                .format_to_object(item)
                .select("ul.ex-list-box > li")
            )
        return items

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
    KingCarArtRunner().run(use_pickled=False)
