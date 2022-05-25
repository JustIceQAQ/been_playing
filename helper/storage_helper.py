import json
import os
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Dict
from uuid import uuid4

from pydantic import BaseModel, Field
from pysondb import db


def hex_uuid4() -> str:
    return uuid4().hex


class Exhibition(BaseModel):
    systematics: str
    title: str
    date: str = None
    address: str = None
    figure: str = None
    source_url: str = None
    UUID: str = Field(default_factory=hex_uuid4)


class StorageInit(metaclass=ABCMeta):
    @abstractmethod
    def create_data(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def read_data(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def truncate_table(self, *args, **kwargs):
        raise NotImplementedError


class JustJsonStorage(StorageInit):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db = Path(db_path)
        new_db_name = f"{str(self.db.name)}"
        self.db_path = self.db_path.replace(self.db.name, new_db_name)
        self.temp_data = []

    def create_data(self, data=None):
        self.temp_data.append(data)

    def commit(self):
        self.fd = open(self.db_path, "w", encoding="utf-8")
        json_object = json.dumps({"data": self.temp_data}, indent=4)
        self.fd.write(json_object)
        self.fd.close()

    def read_data(self, *args, **kwargs):
        pass

    def truncate_table(self, *args, **kwargs):
        if os.path.isfile(self.db_path):
            os.remove(self.db_path)
        self.fd = open(self.db_path, "a", encoding="utf-8")
        self.fd.close()


class PySonDBStorage(StorageInit):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db = db.getDb(db_path)

    def create_data(self, data):
        if isinstance(data, dict):
            self.db.add(data)
        elif isinstance(data, list):
            self.db.addMany(data)

    def read_data(self, count: int = None, filter_dict: Dict = None):
        if count is None:
            return self.db.getAll()
        elif count and isinstance(count, int):
            return self.db.get(count)
        elif filter_dict is not None:
            return self.db.getBy(filter_dict)

    def truncate_table(self):
        if os.path.isfile(self.db_path):
            os.remove(self.db_path)
        self.db = db.getDb(self.db_path)
