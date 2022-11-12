from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Any, Dict, Union

import requests
from retry import retry

from helper.proxy_helper import NoneProxy

requests.adapters.DEFAULT_RETRIES = 5


# 實作各種類型爬蟲
class CrawlerInit(metaclass=ABCMeta):
    @abstractmethod
    def get_page(self, *args, **kwargs):
        raise NotImplementedError


class RequestsCrawler(CrawlerInit):
    class Formatted(str, Enum):
        text = "text"
        json = "json"

    def __init__(self, url: str, module_proxy=NoneProxy):
        self.url = url
        self.rs = requests.session()
        self.rs.keep_alive = False
        self.proxy = None
        self.init_proxy(module_proxy)

    def init_proxy(self, module_proxy):
        if module_proxy:
            self.proxy = module_proxy()
            self.proxy.load_source()
            self.rs.proxies = self.proxy.get_random_proxy()

    def get_cookies(self, method="GET", *args, **kwargs):
        response = self.rs.request(method, self.url, *args, **kwargs)
        return response.cookies

    @retry(tries=5, delay=20, backoff=2, max_delay=500)
    def get_page(
        self, method="GET", reload_session=True, formatted="text", *args, **kwargs
    ) -> Union[Dict[Any, Any], str]:

        if "timeout" not in kwargs.keys():
            kwargs["timeout"] = 60

        if reload_session:
            self.reload_session()

        response = self.rs.request(method, self.url, *args, **kwargs)

        self.observed_step(response, use_this=True)

        if formatted in {self.Formatted.text}:
            return response.text
        elif formatted in {self.Formatted.json}:
            return response.json()

    def observed_step(self, response, use_this=False) -> None:
        if use_this:
            if ("tickets.books" in response.url) and (response.status_code in {403}):
                raise requests.exceptions.ConnectionError()

    def reload_session(self):
        self.rs.cookies.clear()
        self.rs.headers.clear()
        self.rs.proxies = self.proxy.get_random_proxy()


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
