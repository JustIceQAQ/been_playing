from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import MocaTaipeiParse
from helper.storage_helper import Exhibition, JustJsonStorage


def mocataipei_script(use_pickled=False) -> None:
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent"
    target_domain = "https://www.mocataipei.org.tw"
    target_storage = str(root_dir / "data" / "mocataipei_exhibition.json")
    target_systematics = ExhibitionEnum.mocataipei
    target_visit_url = "https://www.mocataipei.org.tw/tw/Visit/%E6%99%82%E9%96%93%E8%88%87%E7%A5%A8%E5%83%B9"

    requests_worker = RequestsBeautifulSoupInstantiation(target_url)
    target_object = requests_worker.fetch()
    storage = JustJsonStorage(target_storage, target_systematics)
    storage.truncate_table()

    dataset = target_object.select("div.listFrameBox div.list")

    for item in dataset:
        mocataipei_data = MocaTaipeiParse(item).parsed(target_domain=target_domain)
        mocataipei_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in mocataipei_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **mocataipei_clean_data)
        storage.create_data(exhibition.dict(), pickled=use_pickled)

    requests_visit = RequestsBeautifulSoupInstantiation(target_visit_url)
    targe_visit_object = requests_visit.fetch()
    visit = targe_visit_object.select_one("section.category > .secBox > p.normal")
    storage.set_visit({"opening": visit.get_text()})
    storage.commit()


if __name__ == "__main__":
    mocataipei_script(use_pickled=False)
