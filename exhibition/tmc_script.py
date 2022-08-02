from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import TMCParse
from helper.storage_helper import Exhibition, JustJsonStorage


def tmc_script() -> None:
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://tmc.taipei/show/event/"
    target_storage = str(root_dir / "data" / "tmc_exhibition.json")
    target_systematics = ExhibitionEnum.tmc

    storage = JustJsonStorage(target_storage)
    storage.truncate_table()

    items = []

    requests_worker = RequestsBeautifulSoupInstantiation(target_url)
    dataset = requests_worker.fetch()
    items.extend(dataset.select(".o-archive-frame__cards > div"))

    pagination__list = dataset.select(".m-pagination__list > div > a")
    paginations = {
        this_pagination
        for pagination in pagination__list
        if (this_pagination := pagination.get("href", ""))
    }
    for pagination_url in paginations:
        requests_worker = RequestsBeautifulSoupInstantiation(pagination_url)
        dataset = requests_worker.fetch()
        items.extend(dataset.select(".o-archive-frame__cards > div"))

    for item in items:
        tcm_data = TMCParse(item).parsed()
        tcm_clean_data = {
            key: RequestsClean.clean_string(value) for key, value in tcm_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **tcm_clean_data)
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    tmc_script()
