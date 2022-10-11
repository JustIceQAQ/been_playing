import json
from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.header_helper import TFAMLifeHeader
from helper.instantiation_helper import (
    RequestsBeautifulSoupInstantiation,
    RequestsJsonInstantiation,
)
from helper.parse_helper import TFAMParse
from helper.storage_helper import Exhibition, JustJsonStorage


def tfam_script(use_pickled=False) -> None:
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.tfam.museum/ashx/Exhibition.ashx?ddlLang=zh-tw"
    target_storage = str(root_dir / "data" / "tfam_exhibition.json")
    target_systematics = ExhibitionEnum.tfam
    target_domain = "https://www.tfam.museum"
    target_visit_url = "https://www.tfam.museum/Common/editor.aspx?id=230&ddlLang=zh-tw"

    storage = JustJsonStorage(target_storage, target_systematics)
    storage.truncate_table()

    requests_worker = RequestsJsonInstantiation(target_url)

    headers = TFAMLifeHeader().get_header()

    dataset_1 = requests_worker.fetch(
        method="POST",
        headers=headers,
        data=json.dumps({"JJMethod": "GetEx", "Type": "1"}),
    )
    dataset_2 = requests_worker.fetch(
        method="POST",
        headers=headers,
        data=json.dumps({"JJMethod": "GetEx", "Type": "2"}),
    )

    dataset_list = []
    dataset_list.extend(dataset_1.get("Data", []))
    dataset_list.extend(dataset_2.get("Data", []))

    for item in dataset_list:
        tfam_data = TFAMParse(item).parsed(target_domain=target_domain)
        tfam_clean_data = {
            key: RequestsClean.clean_string(value) for key, value in tfam_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **tfam_clean_data)
        storage.create_data(exhibition.dict(), pickled=use_pickled)

    requests_visit = RequestsBeautifulSoupInstantiation(target_visit_url)
    targe_visit_object = requests_visit.fetch()
    visit = targe_visit_object.select_one("div.spacingB-20 > .table1")
    storage.set_visit({"opening": str(visit)})
    storage.commit()


if __name__ == "__main__":
    tfam_script(use_pickled=False)
