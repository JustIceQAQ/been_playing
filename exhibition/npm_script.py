from pathlib import Path

from helper.clean_helper import RequestsClean
from helper.parse_helper import NpmColParse, NpmRowParse
from helper.storage_helper import Exhibition, JustJsonStorage
from helper.worker_helper import RequestsWorker


def npm_script():
    ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
    TARGET_URL = "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1"
    TARGET_DOMAIN = "https://www.npm.gov.tw/"
    TARGET_STORAGE = str(ROOT_DIR / "data" / "npm_exhibition.json")
    TARGET_SYSTEMATICS = "npm[故宮]"

    requests_worker = RequestsWorker(TARGET_URL)
    bs4_object = requests_worker.fetch()
    storage = JustJsonStorage(TARGET_STORAGE)
    storage.truncate_table()

    datasets_row = bs4_object.select("ul.mt-4 li.mb-8")
    datasets_col = bs4_object.select("ul.mt-10 li.mb-8")

    for item in datasets_row:
        npm_row_data = NpmRowParse(item).parsed(
            target_domain=TARGET_DOMAIN, used_this_to_clean=RequestsClean.clean_string
        )
        npm_row_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in npm_row_data.items()
        }
        exhibition = Exhibition(systematics=TARGET_SYSTEMATICS, **npm_row_clean_data)
        storage.create_data(exhibition.dict())

    for item in datasets_col:
        npm_col_data = NpmColParse(item).parsed(
            target_domain=TARGET_DOMAIN, used_this_to_clean=RequestsClean.clean_string
        )
        npm_col_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in npm_col_data.items()
        }
        exhibition = Exhibition(systematics=TARGET_SYSTEMATICS, **npm_col_clean_data)
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    npm_script()
