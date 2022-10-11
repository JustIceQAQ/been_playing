from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import NpmColParse, NpmRowParse
from helper.storage_helper import Exhibition, JustJsonStorage


def npm_script(use_pickled=False) -> None:
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1"
    target_domain = "https://www.npm.gov.tw/"
    target_storage = str(root_dir / "data" / "npm_exhibition.json")
    target_systematics = ExhibitionEnum.npm
    target_visit_url = "https://www.npm.gov.tw/Articles.aspx?sno=02007001"

    requests_worker = RequestsBeautifulSoupInstantiation(target_url)
    target_object = requests_worker.fetch()
    storage = JustJsonStorage(target_storage, target_systematics)
    storage.truncate_table()

    datasets_row = target_object.select("ul.mt-4 li.mb-8")
    datasets_col = target_object.select("ul.mt-10 li.mb-8")

    for item in datasets_row:
        npm_row_data = NpmRowParse(item).parsed(
            target_domain=target_domain, used_this_to_clean=RequestsClean.clean_string
        )
        npm_row_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in npm_row_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **npm_row_clean_data)
        storage.create_data(exhibition.dict())

    for item in datasets_col:
        npm_col_data = NpmColParse(item).parsed(
            target_domain=target_domain, used_this_to_clean=RequestsClean.clean_string
        )
        npm_col_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in npm_col_data.items()
        }
        exhibition = Exhibition(systematics=target_systematics, **npm_col_clean_data)
        storage.create_data(exhibition.dict(), pickled=use_pickled)

    requests_visit = RequestsBeautifulSoupInstantiation(target_visit_url)
    targe_visit_object = requests_visit.fetch()
    visit = targe_visit_object.select_one("div.visit-content > p")
    visit_info = "\n".join(
        [
            info_string
            for info in targe_visit_object.select(
                "ul.visit-list > li:nth-child(1) > div.visit-content > ul > li > small"
            )
            if (info_string := info.get_text())
        ]
    )
    storage.set_visit({"opening": visit.get_text() + "\n" + visit_info})

    storage.commit()


if __name__ == "__main__":
    npm_script(use_pickled=False)
