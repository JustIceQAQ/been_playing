from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.ntsec.header import NTSECHeader
from exhibition.ntsec.parse import NTSECParse
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.runner_helper import RunnerInit


class NTSECRunner(RunnerInit):
    """國立臺灣科學教育館"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = "https://www.ntsec.gov.tw/article/list.aspx?a=25"
    use_method = "GET"
    target_domain = "https://www.ntsec.gov.tw"
    target_visit_url = "https://www.ntsec.gov.tw/article/detail.aspx?a=80"
    target_storage = str(root_dir / "data" / "ntsec_exhibition.json")
    target_systematics = ExhibitionEnum.NTSEC
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = NTSECHeader
    use_parse = NTSECParse

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(self.use_method, headers=headers)

    def get_items(self, response):
        # print(response.select("#MainContent_divListItem > a"))
        return response.select("#MainContent_divListItem > a")

    def get_parsed(self, items):
        for item in items:
            data = self.use_parse(item).parsed(target_domain=self.target_domain)
            clean_data = {
                key: RequestsClean.clean_string(value) for key, value in data.items()
            }
            exhibition = self.exhibition_model(
                systematics=self.target_systematics, **clean_data
            )
            # print(exhibition)
            yield exhibition

    def get_visit(self, *args, **kwargs):
        requests_worker = self.instantiation(self.target_visit_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        response = requests_worker.fetch(self.use_method, headers=headers)
        newsin_text = response.find("div", {"class": "newsin-text"})
        title_obj = newsin_text.find("h2")
        title = title_obj.get_text().strip()
        newsin_text_table = newsin_text.find("table", {"class": "newsin-text-table"})
        openings = "\n".join(
            [
                " | ".join([td.get_text().strip() for td in tr.find_all("td")])
                for tr in newsin_text_table.select("tbody > tr")
            ]
        )
        suffix_info = (
            has_suffix_info.get_text().strip()
            if (has_suffix_info := newsin_text_table.next_sibling.next_sibling)
            else ""
        )

        openings_list = [
            title,
            title_obj.next_sibling.get_text().strip(),
            openings,
            suffix_info,
        ]

        return "\n".join(openings_list)


if __name__ == "__main__":
    NTSECRunner().run(use_pickled=False)
    # NTSECRunner().get_visit()
