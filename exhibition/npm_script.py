from helper.worker_helper import RequestsWorker
from helper.clean_helper import RequestsClean
from helper.storage_helper import PySonDBStorage, Exhibition
from pathlib import Path

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
TARGET_URL = "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1"
TARGET_DOMAIN = "https://www.npm.gov.tw/"
TARGET_STORAGE = str(ROOT_DIR / "data" / "npm_exhibition.json")
TARGET_SYSTEMATICS = "npm[故宮]"

requests_worker = RequestsWorker(TARGET_URL)
bs4_object = requests_worker.fetch()
pysondb_storage = PySonDBStorage(TARGET_STORAGE)
pysondb_storage.truncate_table()

datasets_row = bs4_object.select("ul.mt-4 li.mb-8")
datasets_col = bs4_object.select("ul.mt-10 li.mb-8")

for item in datasets_row:
    title = RequestsClean.clean_string(item.find("h3", {"class": "font-medium"}).get_text())
    _date = RequestsClean.clean_string(item.find("div", {"class": "exhibition-list-date"}).get_text())
    address = RequestsClean.clean_string(item.find("div", {"class": "card-content-bottom"}).get_text())
    figure = "{}{}".format(TARGET_DOMAIN, item.select_one("figure.card-image img")["data-src"])
    source_url = "{}{}".format(TARGET_DOMAIN,RequestsClean.clean_string(item.select_one("a.card")["href"]))
    exhibition = Exhibition(
        systematics=TARGET_SYSTEMATICS,
        title=title,
        date=_date,
        address=address,
        figure=figure,
        source_url=source_url
    )
    pysondb_storage.create_data(exhibition.dict())

for item in datasets_col:
    title = RequestsClean.clean_string(item.find("h3", {"class": "card-title-underline"}).get_text())
    _date = RequestsClean.clean_string("-")
    address = RequestsClean.clean_string(item.find("div", {"class": "card-content-bottom"}).get_text())
    figure = "{}{}".format(TARGET_DOMAIN, item.select_one("figure.card-image img")["data-src"])
    source_url = "{}{}".format(TARGET_DOMAIN,RequestsClean.clean_string(item.select_one("a.card")["href"]))
    exhibition = Exhibition(
        systematics=TARGET_SYSTEMATICS,
        title=title,
        date=_date,
        address=address,
        figure=figure,
        source_url=source_url
    )
    pysondb_storage.create_data(exhibition.dict())
