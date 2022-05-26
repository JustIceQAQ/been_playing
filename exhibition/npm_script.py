from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import NpmColParse, NpmRowParse
from helper.storage_helper import Exhibition, JustJsonStorage


def npm_script():
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1"
    target_domain = "https://www.npm.gov.tw/"
    target_storage = str(root_dir / "data" / "npm_exhibition.json")
    target_systematics = ExhibitionEnum.npm

    requests_worker = RequestsBeautifulSoupInstantiation(target_url)
    bs4_object = requests_worker.fetch()
    storage = JustJsonStorage(target_storage)
    storage.truncate_table()

    datasets_row = bs4_object.select("ul.mt-4 li.mb-8")
    datasets_col = bs4_object.select("ul.mt-10 li.mb-8")

    for item in datasets_row:
        npm_row_data = NpmRowParse(item).parsed(
            target_domain=target_domain, used_this_to_clean=RequestsClean.clean_string
        )
        npm_row_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in npm_row_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **npm_row_clean_data)
        storage.create_data(exhibition.dict())

    for item in datasets_col:
        npm_col_data = NpmColParse(item).parsed(
            target_domain=target_domain, used_this_to_clean=RequestsClean.clean_string
        )
        npm_col_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in npm_col_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **npm_col_clean_data)
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    npm_script()
