from pathlib import Path

from helper.clean_helper import RequestsClean
from helper.parse_helper import MocaTaipeiParse
from helper.storage_helper import Exhibition, JustJsonStorage
from helper.worker_helper import RequestsWorker


def mocataipei_script():
    ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
    TARGET_URL = "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent"
    TARGET_DOMAIN = "https://www.mocataipei.org.tw"
    TARGET_STORAGE = str(ROOT_DIR / "data" / "mocataipei_exhibition.json")
    TARGET_SYSTEMATICS = "mocataipei[台北當代藝術館]"

    requests_worker = RequestsWorker(TARGET_URL)
    bs4_object = requests_worker.fetch()
    storage = JustJsonStorage(TARGET_STORAGE)
    storage.truncate_table()

    dataset = bs4_object.select("div.listFrameBox div.list")

    for item in dataset:
        mocataipei_data = MocaTaipeiParse(item).parsed(target_domain=TARGET_DOMAIN)
        mocataipei_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in mocataipei_data.items()
        }

        exhibition = Exhibition(systematics=TARGET_SYSTEMATICS, **mocataipei_clean_data)
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    mocataipei_script()
