from pathlib import Path
from typing import Final

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.header_helper import TicketsBooksHeader
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import TicketsBooksParse
from helper.storage_helper import Exhibition, JustJsonStorage


def tickets_books_script() -> None:
    root_dir: Final = Path(__file__).resolve(strict=True).parent.parent
    target_url: Final = "https://tickets.books.com.tw/leisure/"
    target_storage: Final = str(root_dir / "data" / "books_exhibition.json")
    target_systematics: Final = ExhibitionEnum.tickets_books

    requests_worker = RequestsBeautifulSoupInstantiation(target_url)
    headers = TicketsBooksHeader().get_header()
    response = requests_worker.fetch("GET", headers=headers)
    storage = JustJsonStorage(target_storage)
    storage.truncate_table()

    dataset = response.select("ul.prd > li")

    for item in dataset:
        tickets_books_data = TicketsBooksParse(item).parsed()
        tickets_books_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in tickets_books_data.items()
        }
        exhibition = Exhibition(
            systematics=target_systematics, **tickets_books_clean_data
        )
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    tickets_books_script()
