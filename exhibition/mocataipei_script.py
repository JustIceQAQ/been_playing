from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import MocaTaipeiParse
from helper.storage_helper import Exhibition, JustJsonStorage


def mocataipei_script() -> None:
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent"
    target_domain = "https://www.mocataipei.org.tw"
    target_storage = str(root_dir / "data" / "mocataipei_exhibition.json")
    target_systematics = ExhibitionEnum.mocataipei

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
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    mocataipei_script()
