import logging
import os
import threading
from pathlib import Path

from dotenv import load_dotenv

from exhibition.cksmh_script import CksmhRunner
from exhibition.huashan1914_script import huashan1914_script
from exhibition.jam_script import JamRunner
from exhibition.mocataipei_script import mocataipei_script
from exhibition.museum_post_script import MuseumPostRunner
from exhibition.mwr_script import MWRRunner
from exhibition.nmh_script import NMHRunner
from exhibition.npm_script import npm_script
from exhibition.ntm_script import ntm_script
from exhibition.ntsec_script import ntsec_script
from exhibition.songshanculturalpark_script import songshanculturalpark_script
from exhibition.tfam_script import tfam_script
from exhibition.tickets_books_script import tickets_books_script
from exhibition.tickets_udnfunlife_script import tickets_udnfunlife_script
from exhibition.tmc_script import tmc_script
from exhibition.twtc_script import TWTCRunner
from helper.image_helper import ImgurImage

ROOT_DIR = Path(__file__).resolve(strict=True).parent


def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )

    runtime_logging = logging.getLogger("runtime_logging")

    py_def_scripts = {
        tickets_udnfunlife_script,
        tickets_books_script,
        huashan1914_script,
        mocataipei_script,
        npm_script,
        songshanculturalpark_script,
        ntsec_script,
        tfam_script,
        ntm_script,
        tmc_script,
    }
    py_class_script = {
        CksmhRunner,
        NMHRunner,
        TWTCRunner,
        MWRRunner,
        MuseumPostRunner,
        JamRunner,
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
                target=py_def, name=py_def.__name__, kwargs={"use_pickled": USE_PICKLED}
            )
            for py_def in py_def_scripts
        ]
    )

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
    # print(NMHScript.__name__)
