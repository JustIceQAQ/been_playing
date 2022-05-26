from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.parse_helper import MocaTaipeiParse
from helper.storage_helper import Exhibition, JustJsonStorage
from helper.worker_helper import RequestsWorker


def mocataipei_script():
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent"
    target_domain = "https://www.mocataipei.org.tw"
    target_storage = str(root_dir / "data" / "mocataipei_exhibition.json")
    target_systematics = ExhibitionEnum.mocataipei

    requests_worker = RequestsWorker(target_url)
    bs4_object = requests_worker.fetch()
    storage = JustJsonStorage(target_storage)
    storage.truncate_table()

    dataset = bs4_object.select("div.listFrameBox div.list")

    for item in dataset:
        mocataipei_data = MocaTaipeiParse(item).parsed(target_domain=target_domain)
        mocataipei_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in mocataipei_data.items()
        }

        exhibition = Exhibition(systematics=target_systematics, **mocataipei_clean_data)
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    mocataipei_script()
