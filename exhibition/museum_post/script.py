import time
from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.museum_post.header import MuseumPostHeader
from exhibition.museum_post.parse import MuseumPostParse
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.runner_helper import RunnerInit


class MuseumPostRunner(RunnerInit):
    """郵政博物館"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = "https://museum.post.gov.tw/post/Postal_Museum/museum/index.jsp?ID=131&topage={}"
    permanent_exhibition = "https://museum.post.gov.tw/post/Postal_Museum/museum/index.jsp?ID=136&topage={}"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "museum_post_exhibition.json")
    target_systematics = ExhibitionEnum.MuseumPost
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = MuseumPostHeader
    use_parse = MuseumPostParse
    target_visit_url = (
        "https://museum.post.gov.tw/post/Postal_Museum/museum/index.jsp?ID=141"
    )

    def get_response_check(self, url):
        requests_worker = self.instantiation(url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.fetch(self.use_method, headers=headers)
        time.sleep(2)
        if response.select("ul.part_list > li"):
            return response

    def get_response(self):
        response_target_url = [
            response
            for n in range(1, 5)
            if (response := self.get_response_check(self.target_url.format(n)))
        ]
        response_permanent_exhibition = [
            response
            for n in range(1, 5)
            if (
                response := self.get_response_check(self.permanent_exhibition.format(n))
            )
        ]

        return response_target_url + response_permanent_exhibition

    def get_items(self, response):
        return [data for item in response for data in item.select("ul.part_list > li")]

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
        requests_worker = self.instantiation(self.target_visit_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.fetch(self.use_method, headers=headers)
        opening = response.select_one("ul.article-2")
        if opening is None:
            return None

        return "\n".join(
            [
                opening.select_one("li:nth-child(1) > span.txt").get_text(),
                ";".join(
                    [
                        item.get_text()
                        for item in opening.select(".article-2_item > li > .txt")
                    ]
                ),
            ]
        )


if __name__ == "__main__":
    MuseumPostRunner().run(use_pickled=False)
