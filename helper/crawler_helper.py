from abc import ABCMeta, abstractmethod
from io import BytesIO

import certifi
import pycurl
import requests

# 實作各種類型爬蟲


class CrawlerInit(metaclass=ABCMeta):
    @abstractmethod
    def get_page(self, *args, **kwargs):
        raise NotImplementedError


class RequestsCrawler(CrawlerInit):
    def __init__(self, url: str):
        self.url = url

    def get_page(self) -> str:
        response = requests.get(self.url)
        return response.text


class PyCurlCrawler(CrawlerInit):
    def __init__(self, url: str):
        self.url = url

    def get_page(self) -> str:
        buffer = BytesIO()
        py_curl = pycurl.Curl()
        py_curl.setopt(py_curl.URL, self.url)
        py_curl.setopt(py_curl.WRITEDATA, buffer)
        py_curl.setopt(py_curl.CAINFO, certifi.where())
        py_curl.perform()
        py_curl.close()

        body = buffer.getvalue()
        return body.decode("iso-8859-1")
