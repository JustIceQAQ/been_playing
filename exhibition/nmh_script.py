from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.header_helper import NMHHeader
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import NMHParse
from helper.storage_helper import Exhibition, JustJsonStorage


class NMHScript:
    def __init__(self):
        self.root_dir = Path(__file__).resolve(strict=True).parent.parent
        self.target_url = "https://www.nmh.gov.tw/activitysoonlist_66.html"
        self.use_method = "GET"
        self.target_storage = str(self.root_dir / "data" / "nmh_exhibition.json")
        self.target_systematics = ExhibitionEnum.nmh
        self.instantiation = RequestsBeautifulSoupInstantiation
        self.use_header = NMHHeader
        self.use_parse = NMHParse
        self.use_storage = JustJsonStorage
        self.storage = None
        self.exhibition_model = Exhibition

    def init_storage(self, need_init=True):
        if hasattr(self, "use_storage") and need_init:
            self.storage = self.use_storage(
                self.target_storage, self.target_systematics
            )
            self.storage.truncate_table()

    def write_storage(self, data):
        if self.storage is not None:
            self.storage.create_data(data)

    def commit_storage(self):
        if self.storage is not None:
            self.storage.commit()

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(self.use_method, headers=headers)

    def get_items(self, response):
        return response.select("ul.lists > li.item")

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

    def run(self):
        self.init_storage()
        response = self.get_response()
        items = self.get_items(response)
        exhibitions = self.get_parsed(items)
        for exhibition in exhibitions:
            self.write_storage(exhibition.dict())
        self.commit_storage()


if __name__ == "__main__":
    NMHScript().run()
