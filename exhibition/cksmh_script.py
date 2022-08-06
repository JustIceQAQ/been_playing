from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import CKSMHParse
from helper.storage_helper import Exhibition, JustJsonStorage


def cksmh_script() -> None:
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.cksmh.gov.tw/activitysoonlist_369.html"
    target_storage = str(root_dir / "data" / "cksmh_exhibition.json")
    target_systematics = ExhibitionEnum.cksmh

    requests_worker = RequestsBeautifulSoupInstantiation(target_url)
    target_object = requests_worker.fetch()
    storage = JustJsonStorage(target_storage, target_systematics)
    storage.truncate_table()

    dataset = target_object.select("ul.exhibition-list li dl")

    for item in dataset:
        cksmh_data = CKSMHParse(item).parsed()
        cksmh_clean_data = {
            key: RequestsClean.clean_string(value) for key, value in cksmh_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **cksmh_clean_data)
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    cksmh_script()
