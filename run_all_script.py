import threading
from pathlib import Path

from exhibition.cksmh_script import cksmh_script
from exhibition.huashan1914_script import huashan1914_script
from exhibition.mocataipei_script import mocataipei_script
from exhibition.npm_script import npm_script
from exhibition.ntsec_script import ntsec_script
from exhibition.songshanculturalpark_script import songshanculturalpark_script
from exhibition.tfam_script import tfam_script
from exhibition.tickets_udnfunlife_script import tickets_udnfunlife_script

ROOT_DIR = Path(__file__).resolve(strict=True).parent

if __name__ == "__main__":
    py_scripts = {
        cksmh_script,
        huashan1914_script,
        mocataipei_script,
        npm_script,
        songshanculturalpark_script,
        ntsec_script,
        tfam_script,
        tickets_udnfunlife_script,
    }
    runners = [threading.Thread(target=py_script) for py_script in py_scripts]
    for runner in runners:
        runner.start()
    for runner in runners:
        runner.join()
