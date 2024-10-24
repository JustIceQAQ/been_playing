import dataclasses
import datetime
import json
import os
import uuid
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import IO, Any

import pytz
from dotenv import load_dotenv
from pydantic import BaseModel, Field
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
    title: str | None = None
    date: str | None = None
    address: str | None = None
    figure: str | None = None
    source_url: str
    UUID: str | None = None

    def __init__(self, **kwargs) -> None:
        runtime_kwargs = kwargs
        runtime_kwargs["systematics"] = kwargs.get("systematics").code_name
        super().__init__(**runtime_kwargs)
        self.UUID: str | None = hex_uuid5(self.systematics, self.source_url)


class ExhibitionStorage(BaseModel):
    information: dict | None = Field(default_factory=dict)
    counts: int = 0
    last_update: str | None = None
    data: list[dict[str, str]] | None = Field(default_factory=list)
    visit: dict[str, str] | None = Field(default_factory=dict)


class StorageInit(metaclass=ABCMeta):
    @abstractmethod
    def create_data(self, data, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def read_data(self, *args, **kwargs) -> list[dict[str, Any]] | None:
        raise NotImplementedError

    @abstractmethod
    def truncate_table(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def get_last_update_time(self) -> str:
        # 直接使用UTC
        return datetime.datetime.now(pytz.timezone("UTC")).isoformat()


class JustJsonStorage(StorageInit):
    def __init__(self, db_path: str, exhibition_information: ExhibitionInformation):
        self.fd: IO | None = None
        self.db_path = db_path
        self.db: Path = Path(db_path)
        new_db_name = f"{str(self.db.name)}"
        self.db_path = self.db_path.replace(self.db.name, new_db_name)
        self.temp_data: list[dict[str, str]] = []
        self.ImgurImage = ImgurImage()
        this_env = ROOT_DIR / ".env"
        load_dotenv(this_env)
        client_id = os.getenv("IMGUR_API_CLIENT_ID", False)
        client_secret = os.getenv("IMGUR_API_CLIENT_SECRET", False)
        self.ImgurImage.login(client_id, client_secret)
        self.exhibition_information = exhibition_information
        self.json_object = ExhibitionStorage()
        self.visit = {}
        self.json_object.information = dataclasses.asdict(self.exhibition_information)

    def create_data(self, data: dict[str, str], pickled=True, *args, **kwargs) -> None:
        data["figure"] = (
            self.ImgurImage.upload(data.pop("figure"))
            if pickled
            else data.pop("figure")
        )

        self.temp_data.append(data)

    def set_visit(self, _dict: dict):
        self.visit.update(_dict)

    def commit(self) -> None:
        self.fd = open(self.db_path, "w", encoding="utf-8")
        self.json_object.last_update = self.get_last_update_time()
        self.json_object.counts = len(self.temp_data)
        self.json_object.data = list(
            self.deduplication_but_maintain_sort(key=lambda d: d["UUID"])
        )
        self.json_object.visit = self.visit

        runtime_json_object = json.dumps(
            self.json_object.dict(),
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
        self.fd = open(self.db_path, "w+", encoding="utf-8")
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
        count: int | None = None,
        filter_dict: dict[str, Any] | None = None,
        *args,
        **kwargs,
    ) -> list[dict[str, Any]]:
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
