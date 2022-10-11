from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import HuaShan1914Parse
from helper.storage_helper import Exhibition, JustJsonStorage


def huashan1914_script(use_pickled=False) -> None:
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.huashan1914.com/w/huashan1914/exhibition"
    target_domain = "https://www.huashan1914.com"
    target_storage = str(root_dir / "data" / "huashan1914_exhibition.json")
    target_systematics = ExhibitionEnum.huashan1914

    storage = JustJsonStorage(target_storage, target_systematics)
    storage.truncate_table()

    index = 1
    datasets = []
    while True:
        requests_worker = RequestsBeautifulSoupInstantiation(
            f"{target_url}?index={index}"
        )
        target_object = requests_worker.fetch()
        dataset = target_object.select("ul#event-ul li")
        if dataset:
            datasets.append(dataset)
            index = index + 1
        else:
            break

    for dataset in datasets:
        for item in dataset:
            huashan1914_data = HuaShan1914Parse(item).parsed(
                target_domain=target_domain
            )
            huashan1914_clean_data = {
                key: RequestsClean.clean_string(value)
                for key, value in huashan1914_data.items()
            }

            exhibition = Exhibition(
                systematics=target_systematics, **huashan1914_clean_data
            )
            storage.create_data(exhibition.dict(), pickled=use_pickled)
    storage.commit()


if __name__ == "__main__":
    huashan1914_script(use_pickled=False)
