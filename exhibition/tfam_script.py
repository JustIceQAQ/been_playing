import json
from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.header_helper import TFAMLifeHeader
from helper.instantiation_helper import RequestsJsonInstantiation
from helper.parse_helper import TFAMParse
from helper.storage_helper import Exhibition, JustJsonStorage


def tfam_script() -> None:
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.tfam.museum/ashx/Exhibition.ashx?ddlLang=zh-tw"
    target_storage = str(root_dir / "data" / "tfam_exhibition.json")
    target_systematics = ExhibitionEnum.tfam
    target_domain = "https://www.tfam.museum"

    requests_worker = RequestsJsonInstantiation(target_url)

    headers = TFAMLifeHeader().get_header()

    dataset = requests_worker.fetch(
        method="POST",
        headers=headers,
        data=json.dumps({"JJMethod": "GetEx", "Type": "1"}),
    )
    storage = JustJsonStorage(target_storage)
    storage.truncate_table()

    for item in dataset.get("Data"):
        tfam_data = TFAMParse(item).parsed(target_domain=target_domain)
        tfam_clean_data = {
            key: RequestsClean.clean_string(value) for key, value in tfam_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **tfam_clean_data)
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    tfam_script()
