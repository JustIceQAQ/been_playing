import logging
import os
import threading
from pathlib import Path

from dotenv import load_dotenv

from exhibition.cksmh_script import CKSMHRunner
from exhibition.huashan1914_script import HuaShan1914Runner
from exhibition.jam_script import JamRunner
from exhibition.mocataipei_script import MocaTaipeiRunner
from exhibition.museum_post_script import MuseumPostRunner
from exhibition.mwr_script import MWRRunner
from exhibition.nmh_script import NMHRunner
from exhibition.npm_script import NPMRunner
from exhibition.ntm_script import NTMRunner
from exhibition.ntsec_script import NTSECRunner
from exhibition.songshanculturalpark_script import SongShanCulturalParkRunner
from exhibition.tfam_script import TFAMRunner
from exhibition.tickets_books_script import TicketsBooksRunner
from exhibition.tickets_udnfunlife_script import TicketsUdnFunLifeRunner
from exhibition.tmc_script import TMCRunner
from exhibition.twtc_script import TWTCRunner
from helper.image_helper import ImgurImage


def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )

    runtime_logging = logging.getLogger("runtime_logging")

    py_class_script = {
        CKSMHRunner,
        HuaShan1914Runner,
        JamRunner,
        MWRRunner,
        MocaTaipeiRunner,
        MuseumPostRunner,
        NMHRunner,
        NPMRunner,
        NTMRunner,
        NTSECRunner,
        SongShanCulturalParkRunner,
        TFAMRunner,
        TMCRunner,
        TWTCRunner,
        TicketsBooksRunner,
        TicketsUdnFunLifeRunner,
    }
    ROOT_DIR = Path(__file__).resolve(strict=True).parent
    runtime_logging.debug(ROOT_DIR)

    file_path = ROOT_DIR / "data" / "cache_file.json"
    runtime_logging.debug(file_path)
    imgur_image = ImgurImage()
    imgur_image.load_cache_file(file_path)

    this_env = ROOT_DIR / ".env"
    if this_env.exists():
        runtime_logging.debug(this_env)
        load_dotenv(this_env)
    CLIENT_ID = os.getenv("IMGUR_API_CLIENT_ID", False)
    CLIENT_SECRET = os.getenv("IMGUR_API_CLIENT_SECRET", False)
    USE_PICKLED = os.getenv("USE_PICKLED", True)

    if CLIENT_ID and CLIENT_SECRET:
        imgur_image.login(CLIENT_ID, CLIENT_SECRET)
        runtime_logging.debug("imgur api is logined")

    all_script_runners = []

    all_script_runners.extend(
        [
            threading.Thread(
                target=py_class().run,
                name=py_class.__name__,
                kwargs={"use_pickled": USE_PICKLED},
            )
            for py_class in py_class_script
        ]
    )

    for runner in all_script_runners:
        runner.start()
    runtime_logging.debug("All Script Runners Threading Is Start")

    for runner in all_script_runners:
        runner.join()
    imgur_image.save_cache_file()
    runtime_logging.debug("All Script Runners Threading Is Done")


if __name__ == "__main__":
    main()
