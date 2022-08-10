from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Union

import requests
from simplejson import JSONDecodeError

requests.adapters.DEFAULT_RETRIES = 5


# 實作各種類型爬蟲
class CrawlerInit(metaclass=ABCMeta):
    @abstractmethod
    def get_page(self, *args, **kwargs):
        raise NotImplementedError


class RequestsCrawler(CrawlerInit):
    def __init__(self, url: str):
        self.url = url
        self.rs = requests.session()
        self.rs.keep_alive = False
        self.rs.proxies = {"http": "106.107.205.112:80"}

    def get_page(self, method="GET", *args, **kwargs) -> Union[Dict[Any, Any], str]:
        if "timeout" not in kwargs.keys():
            kwargs["timeout"] = 60

        response = self.rs.request(method, self.url, *args, **kwargs)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text


# class PyCurlCrawler(CrawlerInit):
#     def __init__(self, url: str):
#         self.url = url
#
#     def get_page(self, *args, **kwargs) -> str:
#         # TODO: 補實作 POST
#         buffer = BytesIO()
#         py_curl = pycurl.Curl()
#         py_curl.setopt(py_curl.URL, self.url)
#         py_curl.setopt(py_curl.WRITEDATA, buffer)
#         py_curl.setopt(py_curl.CAINFO, certifi.where())
#         py_curl.perform()
#         py_curl.close()
#
#         body = buffer.getvalue()
#         return body.decode("iso-8859-1")
