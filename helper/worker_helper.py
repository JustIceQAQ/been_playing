from abc import ABCMeta, abstractmethod

import requests
from bs4 import BeautifulSoup


class WorkerInit(metaclass=ABCMeta):
    @abstractmethod
    def get_page(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def format_to_object(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def fetch(self, *args, **kwargs):
        raise NotImplementedError

class RequestsWorker(WorkerInit):
    def __init__(self, url: str):
        self.url = url

    def get_page(self) -> str:
        response = requests.get(self.url)
        return response.text

    def format_to_object(self, text: str, format_encoding="html5lib") -> BeautifulSoup:
        formatted_object = BeautifulSoup(text, format_encoding)
        return formatted_object

    def fetch(self) -> BeautifulSoup:
        response_text = self.get_page()
        formatted_object = self.format_to_object(response_text)
        return formatted_object