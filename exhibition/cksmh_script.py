from pathlib import Path

from helper.clean_helper import RequestsClean
from helper.parse_helper import CKSMHParse
from helper.storage_helper import Exhibition, JustJsonStorage
from helper.worker_helper import RequestsWorker


def cksmh_script():
    ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
    TARGET_URL = "https://www.cksmh.gov.tw/activitysoonlist_369.html"
    TARGET_STORAGE = str(ROOT_DIR / "data" / "cksmh_exhibition.json")
    TARGET_SYSTEMATICS = "cksmh[中正紀念堂]"

    requests_worker = RequestsWorker(TARGET_URL)
    bs4_object = requests_worker.fetch()
    storage = JustJsonStorage(TARGET_STORAGE)
    storage.truncate_table()

    dataset = bs4_object.select("ul.exhibition-list li dl")

    for item in dataset:
        cksmh_data = CKSMHParse(item).parsed()
        cksmh_clean_data = {
            key: RequestsClean.clean_string(value) for key, value in cksmh_data.items()
        }
        exhibition = Exhibition(systematics=TARGET_SYSTEMATICS, **cksmh_clean_data)
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    cksmh_script()
