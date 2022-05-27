import json
from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsJsonInstantiation
from helper.parse_helper import TicketsUdnFunLifeParse
from helper.storage_helper import Exhibition, JustJsonStorage
from helper.translation_helper import BeautifulSoupTranslation


def tickets_udnfunlife_script():
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = (
        "https://tickets.udnfunlife.com/application/UTK01/UTK0101_.aspx/GET_PUSH_LIST"
    )
    target_storage = str(root_dir / "data" / "udnfunlife_exhibition.json")
    target_systematics = ExhibitionEnum.tickets_udnfunlife

    requests_worker = RequestsJsonInstantiation(target_url)
    user_agent = (
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/102.0.5005.61 Safari/537.36"
    )
    headers = {
        "User-Agent": user_agent,
        "Host": "tickets.udnfunlife.com",
        "Origin": "https://tickets.udnfunlife.com",
        "Referer": "https://tickets.udnfunlife.com/application/UTK01/UTK0101_.aspx",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }
    response = requests_worker.fetch(
        method="POST",
        headers=headers,
        data=json.dumps({"pageNo": "1", "pageSize": "100"}),
    )
    storage = JustJsonStorage(target_storage)
    storage.truncate_table()
    dataset = (
        BeautifulSoupTranslation()
        .format_to_object(response["d"]["ReturnData"]["script"])
        .select("div.inner")
    )
    for item in dataset:
        udnfunlife_data = TicketsUdnFunLifeParse(item).parsed()
        udnfunlife_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in udnfunlife_data.items()
        }

        exhibition = Exhibition(systematics=target_systematics, **udnfunlife_clean_data)
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    tickets_udnfunlife_script()
