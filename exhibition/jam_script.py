from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.header_helper import JamHeader
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import JamParse
from helper.runner_helper import RunnerInit


class JamRunner(RunnerInit):
    """忠泰美術館"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "http://jam.jutfoundation.org.tw/online-exhibition"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "jam_exhibition.json")
    target_systematics = ExhibitionEnum.Jam
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = JamHeader
    use_parse = JamParse
    target_visit_url = "http://jam.jutfoundation.org.tw/visit/info"

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        qq = requests_worker.fetch(self.use_method, headers=headers)
        return qq

    def get_items(self, response):
        return response.select("div.view-content > div.views-row")

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
        opening = response.select_one("div.bu-time")
        opening_div = opening.find_all("div")
        info = ""
        if opening_div is not None:
            info += "\n".join([i.get_text() for i in opening_div[:2]])

        opening = response.select_one(
            "div.field.field-name-body.field-type-text-with-summary.field-label-hidden.view-mode-full > div > div"
        )
        info2 = opening.find("strong").parent.next_sibling.next_sibling.get_text()

        return info + "\n" + info2


if __name__ == "__main__":
    JamRunner().run(use_pickled=False)
