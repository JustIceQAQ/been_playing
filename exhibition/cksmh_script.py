from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import CKSMHParse
from helper.storage_helper import Exhibition, JustJsonStorage


def cksmh_script(use_pickled=False) -> None:
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.cksmh.gov.tw/activitysoonlist_369_{}.html"
    target_storage = str(root_dir / "data" / "cksmh_exhibition.json")
    target_systematics = ExhibitionEnum.cksmh
    target_visit_url = "https://www.cksmh.gov.tw/content_78.html"

    storage = JustJsonStorage(target_storage, target_systematics)
    storage.truncate_table()

    dataset_list = []

    requests_worker = RequestsBeautifulSoupInstantiation(target_url.format("1"))
    target_object = requests_worker.fetch()
    dataset_list.extend(target_object.select("ul.exhibition-list li dl"))

    for n in range(2, 5):
        requests_worker = RequestsBeautifulSoupInstantiation(target_url.format(n))
        target_object = requests_worker.fetch()
        if dataset := target_object.select("ul.exhibition-list li dl"):
            dataset_list.extend(dataset)
        else:
            break

    for item in dataset_list:
        cksmh_data = CKSMHParse(item).parsed()
        cksmh_clean_data = {
            key: RequestsClean.clean_string(value) for key, value in cksmh_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **cksmh_clean_data)
        storage.create_data(exhibition.dict(), pickled=use_pickled)

    requests_visit = RequestsBeautifulSoupInstantiation(target_visit_url)
    targe_visit_object = requests_visit.fetch()
    visit = targe_visit_object.select_one("div.zhanjian > div.cont_info > p")
    storage.set_visit({"opening": visit.get_text()})

    storage.commit()


if __name__ == "__main__":
    cksmh_script(use_pickled=False)
