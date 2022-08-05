from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Union

import requests
from simplejson import JSONDecodeError


# 實作各種類型爬蟲
class CrawlerInit(metaclass=ABCMeta):
    @abstractmethod
    def get_page(self, *args, **kwargs):
        raise NotImplementedError


class RequestsCrawler(CrawlerInit):
    def __init__(self, url: str):
        self.url = url

    def get_page(self, method="GET", *args, **kwargs) -> Union[Dict[Any, Any], str]:
        response = requests.request(method, self.url, *args, **kwargs)
        # print(response)
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
