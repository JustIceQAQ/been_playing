from helper.clean_helper import RequestsClean
from helper.storage_helper import PySonDBStorage, Exhibition
from pathlib import Path

from helper.worker_helper import RequestsWorker

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
TARGET_URL = "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent"
TARGET_DOMAIN = "https://www.mocataipei.org.tw"
TARGET_STORAGE = str(ROOT_DIR / "data" / "mocataipei_exhibition.json")
TARGET_SYSTEMATICS = "mocataipei[台北當代藝術館]"

requests_worker = RequestsWorker(TARGET_URL)
bs4_object = requests_worker.fetch()
pysondb_storage = PySonDBStorage(TARGET_STORAGE)
pysondb_storage.truncate_table()

dataset = bs4_object.select("div.listFrameBox div.list")

for item in dataset:
    title = RequestsClean.clean_string(item.find("h3", {"class": "imgTitle"}).get_text())
    _date = RequestsClean.clean_string(item.find("div", {"class": "dateBox"}).get_text())
    address = RequestsClean.clean_string("-")
    figure = "{}{}".format(TARGET_DOMAIN, item.select_one("figure.imgFrame img")["data-src"])
    source_url = RequestsClean.clean_string(item.select_one("a.textFrame")["href"])
    exhibition = Exhibition(
        systematics=TARGET_SYSTEMATICS,
        title=title,
        date=_date,
        address=address,
        figure=figure,
        source_url=source_url
    )
    pysondb_storage.create_data(exhibition.dict())
