from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Union

import requests
from retry import retry
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
        self.rs.proxies = {"http": "106.107.203.151:80"}

    @retry(
        requests.exceptions.ConnectionError, tries=5, delay=30, backoff=2, max_delay=500
    )
    def get_page(self, method="GET", *args, **kwargs) -> Union[Dict[Any, Any], str]:
        if "timeout" not in kwargs.keys():
            kwargs["timeout"] = 60
        self.reload_session()

        response = self.rs.request(method, self.url, *args, **kwargs)
        self.observed_step(response, use_this=True)
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def observed_step(self, response, use_this=False) -> None:
        if use_this:
            if "tickets.books" in response.url:
                print(response.cookies)
                if response.status_code in {403}:
                    raise requests.exceptions.ConnectionError()

    def reload_session(self):
        self.rs = requests.session()
        self.rs.keep_alive = False
        self.rs.proxies = {"http": "106.107.203.151:80"}


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
