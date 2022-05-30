from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import NTSECParse
from helper.storage_helper import Exhibition, JustJsonStorage


def ntsec_script() -> None:
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.ntsec.gov.tw/User/Exhibitions.aspx?a=44"
    target_domain = "https://www.ntsec.gov.tw"
    target_storage = str(root_dir / "data" / "ntsec_exhibition.json")
    target_systematics = ExhibitionEnum.ntsec

    requests_worker = RequestsBeautifulSoupInstantiation(target_url)
    target_object = requests_worker.fetch()
    storage = JustJsonStorage(target_storage)
    storage.truncate_table()

    dataset = target_object.select("#ctl00_artContent > ul > li")
    for item in dataset:
        ntsec_data = NTSECParse(item).parsed(target_domain=target_domain)
        ntsec_clean_data = {
            key: RequestsClean.clean_string(value) for key, value in ntsec_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **ntsec_clean_data)
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    ntsec_script()
