import dataclasses
import datetime
import json
import os
import uuid
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import IO, Any, Dict, List, Optional

import pytz
from dotenv import load_dotenv
from pydantic import BaseModel
from pysondb import db

from exhibition import ExhibitionInformation
from helper.image_helper import ImgurImage

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent


def hex_uuid5(systematics: str, value: str) -> str:
    """
    > It takes a string, and returns a string

    :param systematics: str
    :type systematics: str
    :param value: The value to be hashed
    :type value: str
    :return: A hexadecimal string.
    """

    this_o_uuid = uuid.uuid5(
        uuid.UUID("00000000-0000-0000-0000-000000000000"), systematics
    )
    return uuid.uuid5(this_o_uuid, value).hex


class Exhibition(BaseModel):
    systematics: str
    title: Optional[str] = None
    date: Optional[str] = None
    address: Optional[str] = None
    figure: Optional[str] = None
    source_url: str
    UUID: Optional[str] = None

    def __init__(self, **kwargs) -> None:
        runtime_kwargs = kwargs
        runtime_kwargs["systematics"] = kwargs.get("systematics").code_name
        super().__init__(**runtime_kwargs)
        self.UUID: Optional[str] = hex_uuid5(self.systematics, self.source_url)


class StorageInit(metaclass=ABCMeta):
    @abstractmethod
    def create_data(self, data, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def read_data(self, *args, **kwargs) -> Optional[List[Dict[str, Any]]]:
        raise NotImplementedError

    @abstractmethod
    def truncate_table(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def get_last_update_time(self) -> str:
        # 直接使用UTC
        return datetime.datetime.now(pytz.timezone("UTC")).isoformat()


class JustJsonStorage(StorageInit):
    def __init__(self, db_path: str, exhibition_information: ExhibitionInformation):
        self.fd: Optional[IO] = None
        self.db_path = db_path
        self.db: Path = Path(db_path)
        new_db_name = f"{str(self.db.name)}"
        self.db_path = self.db_path.replace(self.db.name, new_db_name)
        self.temp_data: List[Dict[str, str]] = []
        self.ImgurImage = ImgurImage()
        this_env = ROOT_DIR / ".env"
        load_dotenv(this_env)
        client_id = os.getenv("IMGUR_API_CLIENT_ID", False)
        client_secret = os.getenv("IMGUR_API_CLIENT_SECRET", False)
        self.ImgurImage.login(client_id, client_secret)
        self.exhibition_information = exhibition_information
        self.json_object = {}
        self.visit = {}

    def create_data(self, data: Dict[str, str], pickled=True, *args, **kwargs) -> None:
        data["figure"] = (
            self.ImgurImage.upload(data.pop("figure"))
            if pickled
            else data.pop("figure")
        )
        self.temp_data.append(data)

    def set_visit(self, _dict: Dict):
        self.visit.update(_dict)

    def commit(self) -> None:
        self.fd = open(self.db_path, "w", encoding="utf-8")

        self.json_object = {
            "information": dataclasses.asdict(self.exhibition_information),
            "counts": len(self.temp_data),
            "last_update": self.get_last_update_time(),
            "data": list(self.deduplication_but_maintain_sort(key=lambda d: d["UUID"])),
            "visit": self.visit,
        }
        runtime_json_object = json.dumps(
            self.json_object,
            indent=4,
        )
        self.fd.write(runtime_json_object)
        self.fd.close()

    def deduplication_but_maintain_sort(self, key=None):
        seen = set()
        for item in self.temp_data:
            val = item if key is None else key(item)
            if val not in seen:
                yield item
                seen.add(val)

    def is_have_created_data(self) -> bool:
        return bool(self.temp_data)

    def read_data(self, *args, **kwargs) -> None:
        pass

    def truncate_table(self, *args, **kwargs) -> None:
        if os.path.isfile(self.db_path):
            os.remove(self.db_path)
        self.fd = open(self.db_path, "a", encoding="utf-8")
        self.fd.close()


class PySonDBStorage(StorageInit):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db = db.getDb(db_path)

    def create_data(self, data, *args, **kwargs) -> None:
        if isinstance(data, dict):
            self.db.add(data)
        elif isinstance(data, list):
            self.db.addMany(data)
        else:
            pass

    def read_data(
        self,
        count: Optional[int] = None,
        filter_dict: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        if count is None:
            return self.db.getAll()
        elif count and isinstance(count, int):
            return self.db.get(count)
        elif filter_dict is not None:
            return self.db.getBy(filter_dict)
        else:
            return self.db.getAll()

    def truncate_table(self, *args, **kwargs) -> None:
        if os.path.isfile(self.db_path):
            os.remove(self.db_path)
        self.db = db.getDb(self.db_path)
