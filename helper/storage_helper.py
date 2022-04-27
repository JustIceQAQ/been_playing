import os
from abc import ABCMeta, abstractmethod
from typing import Dict
from pydantic import BaseModel

from pysondb import db


class Exhibition(BaseModel):
    systematics: str
    title: str
    date: str = None
    address: str = None
    figure: str = None
    source_url: str = None


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
