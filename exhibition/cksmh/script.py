from pathlib import Path

from exhibition import ExhibitionEnum
from exhibition.cksmh.parse import CKSMHParse2
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.runner_helper import RunnerInit


class CKSMHRunner(RunnerInit):
    """中正紀念堂"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = "https://www.cksmh.gov.tw/activitysoonlist_369_{}.html"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "cksmh_exhibition.json")
    target_systematics = ExhibitionEnum.CKSMH
    target_visit_url = "https://www.cksmh.gov.tw/content_78.html"
    instantiation = RequestsBeautifulSoupInstantiation
    use_parse = CKSMHParse2
    use_header = None

    # def get_response(self):
    #     dataset_list = []
    #     item_css_selector = "ul.exhibition-list li dl"
    #     requests_worker = self.instantiation(self.target_url.format("1"))
    #     target_object = requests_worker.fetch()
    #     dataset_list.extend(target_object.select(item_css_selector))
    #
    #     self.get_more_range_with_url(dataset_list, item_css_selector)
    #     return dataset_list
    def get_response(self):
        requests_worker = self.instantiation(
            "https://www.cksmh.gov.tw/News_Actives_photo.aspx?n=6067&sms=14954"
        )
        target_object = requests_worker.fetch()
        return target_object

    def get_more_range_with_url(self, dataset_list, item_css_selector):
        for n in range(2, 5):
            requests_worker = self.instantiation(self.target_url.format(n))
            target_object = requests_worker.fetch()
            if dataset := target_object.select(item_css_selector):
                dataset_list.extend(dataset)
            else:
                break

    def get_items(self, response):
        div = response.select_one("div.group-list.page-block")
        data = div.find("ul").find_all("li")
        return data

    def get_parsed(self, items):
        for item in items:
            data = self.use_parse(item).parsed()
            if data["source_url"] is None:
                continue
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
        opening = response.select_one("div.zhanjian > div.cont_info > p")
        return None if opening is None else opening.get_text()


if __name__ == "__main__":
    CKSMHRunner().run(use_pickled=False)
