from enum import Enum
from pathlib import Path
from typing import Any

import requests
from retry import retry

from helper.crawler import CrawlerInit
from helper.proxy_helper import FreeProxy, NoneProxy


class RequestsCrawler(CrawlerInit):
    class Formatted(str, Enum):
        text = "text"
        json = "json"

    def __init__(self, url: str, module_proxy: NoneProxy | FreeProxy = NoneProxy):
        self.url = url
        self.rs = requests.session()
        self.rs.keep_alive = False
        self.proxy = None
        self.init_proxy(module_proxy)

    def init_proxy(self, module_proxy):
        if module_proxy:
            self.proxy = module_proxy()
            self.proxy.load_source(
                proxy_path=Path(__file__).parent.parent.parent.absolute()
                / "fixture"
                / "proxy.pkl"
            )
            self.rs.proxies = self.proxy.get_random_proxy()

    def get_cookies(self, method="GET", *args, **kwargs):
        response = self.rs.request(method, self.url, *args, **kwargs)
        return response.cookies

    @retry(tries=5, delay=20, backoff=2, max_delay=500)
    def get_page(
        self, method="GET", reload_session=True, formatted="text", *args, **kwargs
    ) -> dict[Any, Any] | str:

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
