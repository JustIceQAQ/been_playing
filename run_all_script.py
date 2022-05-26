import threading
from pathlib import Path

from exhibition.cksmh_script import cksmh_script
from exhibition.huashan1914_script import huashan1914_script
from exhibition.mocataipei_script import mocataipei_script
from exhibition.npm_script import npm_script
from exhibition.songshanculturalpark import songshanculturalpark_script

ROOT_DIR = Path(__file__).resolve(strict=True).parent

if __name__ == "__main__":
    py_scripts = {
        cksmh_script,
        huashan1914_script,
        mocataipei_script,
        npm_script,
        songshanculturalpark_script,
    }
    runners = [threading.Thread(target=py_script) for py_script in py_scripts]
    for runner in runners:
        runner.start()
    for runner in runners:
        runner.join()
