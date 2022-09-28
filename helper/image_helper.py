import hashlib
import json
import logging
import os
import threading
import time
from abc import ABCMeta
from pathlib import Path
from threading import Lock
from typing import Dict

from dotenv import load_dotenv
from imgurpython import ImgurClient

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
runtime_logging = logging.getLogger("runtime_logging")


class ImageInit(metaclass=ABCMeta):
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def login(*args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def upload(*args, **kwargs):
        raise NotImplementedError


class ImgurImage(ImageInit):
    cache_data: Dict = {}
    client = None
    cache_file = None
    cache_file_path = None

    def webp_format(self, image_id):
        return f"https://i.imgur.com/{image_id}.webp"

    def login(self, client_id, client_secret):
        self.client = ImgurClient(client_id, client_secret)

    def upload(self, image_url, config=None, anon=True):
        runtime_url = image_url
        hash_url = hashlib.md5(image_url.encode("utf-8")).hexdigest()
        runtime_logging.debug(
            f"{threading.current_thread().name}: will be upload {hash_url} {runtime_url}"
        )
        try:
            if hash_url not in self.cache_data.keys():
                with self._lock:
                    runtime_logging.debug(
                        f"{threading.current_thread().name}: get authority now upload {hash_url}"
                    )

                    response = self.client.upload_from_url(
                        runtime_url, config=config, anon=anon
                    )
                    if image_id := response.get("id"):
                        runtime_logging.debug(
                            f"{threading.current_thread().name}: upload {hash_url} is success"
                        )

                        runtime_url = self.webp_format(image_id)
                        self.commit_data({hash_url: runtime_url})

                        runtime_logging.debug(
                            f"{threading.current_thread().name}: commit uploaded {hash_url} data is success"
                        )
                        time.sleep(8)
            else:
                runtime_logging.debug(
                    f"{threading.current_thread().name}: {hash_url} is   "
                )
                runtime_url = self.cache_data.get(hash_url)
        except Exception as ex:
            runtime_logging.debug(f"{threading.current_thread().name}: {ex}")
        return runtime_url

    def load_cache_file(self, path: Path = None):
        self.cache_file_path = (
            str(ROOT_DIR / "data" / "cache_file.json") if path is None else str(path)
        )
        with open(self.cache_file_path, encoding="utf-8") as file:
            self.cache_data = json.load(file)

    def commit_data(self, data: Dict):
        self.cache_data.update(data)

    def save_cache_file(self):
        with open(self.cache_file_path, "w", encoding="utf-8") as file:
            json.dump(self.cache_data, file, indent=4)


if __name__ == "__main__":
    # print(ROOT_DIR)
    imgur_image = ImgurImage()
    imgur_image.load_cache_file()

    this_env = ROOT_DIR / ".env"
    load_dotenv(this_env)

    CLIENT_ID = os.getenv("IMGUR_API_CLIENT_ID", False)
    CLIENT_SECRET = os.getenv("IMGUR_API_CLIENT_SECRET", False)

    if CLIENT_ID and CLIENT_SECRET:
        imgur_image = ImgurImage()
        imgur_image.login(CLIENT_ID, CLIENT_SECRET)

        credits = imgur_image.client.get_credits()

        # print(credits)

        image_url = ".png"
        datas = imgur_image.upload(image_url)
        # print(datas)
    imgur_image.save_cache_file()
