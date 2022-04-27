from worker_helper import RequestsWorker
from clean_helper import RequestsClean
from storage_helper import PySonDBStorage

requests_worker = RequestsWorker("https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1")
bs4_object = requests_worker.fetch()
pysondb_storage = PySonDBStorage("npm_exhibition.json")
pysondb_storage.truncate_table()

datasets_row = bs4_object.select("ul.mt-4 li.mb-8")
datasets_col = bs4_object.select("ul.mt-10 li.mb-8")

for item in datasets_row:
    title = RequestsClean.clean_string(item.find("h3", {"class": "font-medium"}).get_text())
    _date = RequestsClean.clean_string(item.find("div", {"class": "exhibition-list-date"}).get_text())
    address = RequestsClean.clean_string(item.find("div", {"class": "card-content-bottom"}).get_text())
    figure = "https://www.npm.gov.tw/{}".format(item.select_one("figure.card-image img")["data-src"])
    pysondb_storage.create_data({
        "title": title,
        "date": _date,
        "address": address,
        "figure": figure,
    })

for item in datasets_col:
    title = RequestsClean.clean_string(item.find("h3", {"class": "card-title-underline"}).get_text())
    _date = RequestsClean.clean_string("-")
    address = RequestsClean.clean_string(item.find("div", {"class": "card-content-bottom"}).get_text())
    figure = "https://www.npm.gov.tw/{}".format(item.select_one("figure.card-image img")["data-src"])
    pysondb_storage.create_data({
        "title": title,
        "date": _date,
        "address": address,
        "figure": figure,
    })
