from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.parse_helper import SongShanCulturalParkParse
from helper.storage_helper import Exhibition, JustJsonStorage


def songshanculturalpark_script(use_pickled=False) -> None:
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.songshanculturalpark.org/exhibition"
    target_domain = "https://www.songshanculturalpark.org"
    target_storage = str(root_dir / "data" / "songshanculturalpark_exhibition.json")
    target_systematics = ExhibitionEnum.songshanculturalpark

    storage = JustJsonStorage(target_storage, target_systematics)
    storage.truncate_table()
    requests_worker = RequestsBeautifulSoupInstantiation(target_url)
    target_object = requests_worker.fetch()
    dataset = target_object.select("div#exhibition > div.rows")
    for item in dataset:
        songshanculturalpark_data = SongShanCulturalParkParse(item).parsed(
            target_domain=target_domain
        )
        songshanculturalpark_clean_data = {
            key: RequestsClean.clean_string(value)
            for key, value in songshanculturalpark_data.items()
        }

        exhibition = Exhibition(
            systematics=target_systematics, **songshanculturalpark_clean_data
        )
        storage.create_data(exhibition.dict(), pickled=use_pickled)
    storage.commit()


if __name__ == "__main__":
    songshanculturalpark_script(use_pickled=False)
