from pathlib import Path
from typing import Final

from exhibition import ExhibitionEnum
from exhibition.tickets_books.header import TicketsBooksHeader
from exhibition.tickets_books.parse import TicketsBooksParse
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.runner_helper import RunnerInit


class TicketsBooksRunner(RunnerInit):
    """博客來售票網"""

    root_dir: Final = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url: Final = "https://tickets.books.com.tw/leisure/"
    use_method = "GET"
    target_storage: Final = str(root_dir / "data" / "books_exhibition.json")
    target_systematics: Final = ExhibitionEnum.TicketsBooks
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = TicketsBooksHeader
    use_parse = TicketsBooksParse

    def get_response(self):
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(self.use_method, headers=headers)

    def get_items(self, response):
        return response.select("ul.prd > li")

    def get_parsed(self, items):
        for item in items:
            data = self.use_parse(item).parsed()
            clean_data = {
                key: RequestsClean.clean_string(value) for key, value in data.items()
            }
            exhibition = self.exhibition_model(
                systematics=self.target_systematics, **clean_data
            )
            yield exhibition


if __name__ == "__main__":
    TicketsBooksRunner().run(use_pickled=False)
