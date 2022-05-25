from helper.clean_helper import RequestsClean
from helper.parse_helper import CKSMHParse
from helper.storage_helper import PySonDBStorage, Exhibition
from pathlib import Path

from helper.worker_helper import RequestsWorker

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
TARGET_URL = "https://www.cksmh.gov.tw/activitysoonlist_369.html"
TARGET_DOMAIN = "https://www.cksmh.gov.tw"
TARGET_STORAGE = str(ROOT_DIR / "data" / "cksmh_exhibition.json")
TARGET_SYSTEMATICS = "cksmh[中正紀念堂]"

requests_worker = RequestsWorker(TARGET_URL)
bs4_object = requests_worker.fetch()
pysondb_storage = PySonDBStorage(TARGET_STORAGE)
pysondb_storage.truncate_table()

dataset = bs4_object.select("ul.exhibition-list li dl")

for item in dataset:
    cksmh_data = CKSMHParse(item).parsed()
    cksmh_clean_data = {key: RequestsClean.clean_string(value) for key, value in cksmh_data.items()}
    exhibition = Exhibition(
        systematics=TARGET_SYSTEMATICS,
        **cksmh_clean_data
    )
    pysondb_storage.create_data(exhibition.dict())
