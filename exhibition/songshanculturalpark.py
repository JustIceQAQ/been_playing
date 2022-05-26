from pathlib import Path

from exhibition import ExhibitionEnum
from helper.clean_helper import RequestsClean
from helper.parse_helper import SongShanCulturalParkParse
from helper.storage_helper import Exhibition, JustJsonStorage
from helper.worker_helper import RequestsWorker


def songshanculturalpark_script():
    root_dir = Path(__file__).resolve(strict=True).parent.parent
    target_url = "https://www.songshanculturalpark.org/exhibition"
    target_domain = "https://www.songshanculturalpark.org"
    target_storage = str(root_dir / "data" / "songshanculturalpark_exhibition.json")
    target_systematics = ExhibitionEnum.songshanculturalpark

    storage = JustJsonStorage(target_storage)
    storage.truncate_table()
    requests_worker = RequestsWorker(target_url)
    bs4_object = requests_worker.fetch()
    dataset = bs4_object.select("div#exhibition > div.rows")
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
        storage.create_data(exhibition.dict())
    storage.commit()


if __name__ == "__main__":
    songshanculturalpark_script()
