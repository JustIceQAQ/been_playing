import hashlib
import io
import json
from typing import Optional
from helper.storage import StorageInit
from httpx import Client
from threading import Lock
from pathlib import Path


class ImgurStorage(StorageInit):
    _lock: Lock = Lock()
    _root_uri = "https://api.imgur.com/3"
    _uploaded_image_url = "https://i.imgur.com/{}.webp"
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, cache_file_path: Optional[Path] = None, use_cache: Optional[bool] = True):
        self._client_id: Optional[str] = None
        self._client_secret: Optional[str] = None
        self._authorization: Optional[str] = None
        self._cache_file_path = cache_file_path or Path(__file__).resolve(strict=True).parent.parent.parent.parent
        self._client = Client()
        self._temp_cache_data: Optional[dict] = None
        self.use_cache = use_cache

    def _load_cache_data(self):
        with open(self._cache_file_path / Path("data/cache_file.json"), "a+", encoding="utf-8") as file:
            file.seek(0)
            try:
                self._temp_cache_data = json.load(file)
            except io.UnsupportedOperation:
                self._temp_cache_data = {}

    def _update_cache_data(self, data: dict):
        self._temp_cache_data.update(data)

    def _dump_cache_data(self):
        with open(self._cache_file_path / Path("data/cache_file.json"), "w", encoding="utf-8") as file:
            json.dump(self._temp_cache_data, file, indent=4)
        del self._temp_cache_data
        self._temp_cache_data = None

    def _get_cache_url(self, image_url_hash: str) -> Optional[str]:
        self._load_cache_data()
        return self._temp_cache_data.get(image_url_hash, None)

    def _cache_data_process(self, image_url_hash: str, image_id: str):
        self._load_cache_data()
        self._update_cache_data({image_url_hash: image_id})
        self._dump_cache_data()

    def login(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._client.headers.update({"Authorization": f"Client-ID {self._client_id}"})

    def upload(self, image_url: Optional[str]) -> Optional[str]:
        """

        Args:
            image_url:

        Returns:
            url "https://i.imgur.com/{id}.webp" or None

        """
        if image_url is None:
            return image_url

        image_url_hash = hashlib.md5(image_url.encode("utf-8")).hexdigest()
        with self._lock:
            if (formatted_uri := self._get_cache_url(image_url_hash)) is not None:
                return formatted_uri

            payload = {'image': image_url, "type": "URL"}
            response = self._client.post(f"{self._root_uri}/image", data=payload)
            if response.is_success:
                result = response.json()
                formatted_uri = self._uploaded_image_url.format(result.get("data").get("id"))
                if self.use_cache:
                    self._cache_data_process(image_url_hash, formatted_uri)
                return formatted_uri
            return None


if __name__ == '__main__':
    imgur_storage = ImgurStorage()
    imgur_storage.login("2018b51376bdb4d", "649d4b34ef0c13db1d86823bda1516f3ea477cee")
    qaq = imgur_storage.upload(
        "https://event.culture.tw/userFiles/NMH/JpgFile/01/30046/AD/30046_0_0_234955_276_175.jpg")
    print(qaq)
