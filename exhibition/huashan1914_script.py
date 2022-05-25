from pathlib import Path

from helper.clean_helper import RequestsClean
from helper.parse_helper import HuaShan1914Parse
from helper.storage_helper import Exhibition, JustJsonStorage
from helper.worker_helper import RequestsWorker


def huashan1914_script():
    ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
    TARGET_URL = "https://www.huashan1914.com/w/huashan1914/exhibition"
    TARGET_DOMAIN = "https://www.huashan1914.com"
    TARGET_STORAGE = str(ROOT_DIR / "data" / "huashan1914_exhibition.json")
    TARGET_SYSTEMATICS = "huashan1914[華山1914]"

    storage = JustJsonStorage(TARGET_STORAGE)
    storage.truncate_table()

    index = 1
    datasets = []
    while True:
        requests_worker = RequestsWorker(f"{TARGET_URL}?index={index}")
        bs4_object = requests_worker.fetch()
        dataset = bs4_object.select("ul#event-ul li")
        if dataset:
            datasets.append(dataset)
            index = index + 1
        else:
            break

    for dataset in datasets:
        for item in dataset:
            huashan1914_data = HuaShan1914Parse(item).parsed(
                target_domain=TARGET_DOMAIN
            )
            huashan1914_clean_data = {
                key: RequestsClean.clean_string(value)
                for key, value in huashan1914_data.items()
            }

            exhibition = Exhibition(
                systematics=TARGET_SYSTEMATICS, **huashan1914_clean_data
            )
            storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    huashan1914_script()
