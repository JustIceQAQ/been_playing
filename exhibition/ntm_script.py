from itertools import chain, product
from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import NTMParse
from helper.storage_helper import Exhibition, JustJsonStorage


def ntm_script() -> None:
    target_domain = "https://www.ntm.gov.tw"
    urls_format = "{}/exhibitionlist_{}.html?Type={}"

    root_dir = Path(__file__).resolve(strict=True).parent.parent
    product_data = product(
        ("179", "182", "185", "383", "380"),
        (
            "PE1",
            "SP1",
        ),
    )
    target_urls = list(
        urls_format.format(target_domain, *item) for item in product_data
    )
    target_storage = str(root_dir / "data" / "ntm_exhibition.json")
    target_systematics = ExhibitionEnum.ntm

    requests_workers = list(
        RequestsBeautifulSoupInstantiation(target_url) for target_url in target_urls
    )
    target_objects = list(
        requests_worker.fetch() for requests_worker in requests_workers
    )
    storage = JustJsonStorage(target_storage, target_systematics)
    storage.truncate_table()

    dataset = chain.from_iterable(
        target_object.select("#exhibition-list > dl")
        for target_object in target_objects
    )
    for item in list(dataset):

        ntsec_data = NTMParse(item).parsed()
        ntsec_clean_data = {
            key: RequestsClean.clean_string(value) for key, value in ntsec_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **ntsec_clean_data)
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    ntm_script()
