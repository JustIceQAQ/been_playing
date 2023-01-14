import dataclasses
import logging
import os
import time
from abc import ABCMeta, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Union

import requests
from dotenv import load_dotenv
from retry import retry

from helper.proxy_helper import NoneProxy

requests.adapters.DEFAULT_RETRIES = 5

logging.basicConfig(level=logging.DEBUG)


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


class ScraperApiCrawler(CrawlerInit):
    def __init__(self, api_key=None, api_path="http://api.scraperapi.com"):
        self.api_key = self.__set_api_key(api_key)
        self.rs = requests.session()
        self.api_path = api_path

    def __set_api_key(self, api_key):
        if api_key is None:
            raise ValueError
        return api_key

    def get_page(self, url, render=True):
        payload = {"api_key": self.api_key, "url": url, "render": render}
        return self.rs.get(self.api_path, params=payload)


class ScraperAsyncApiCrawler(CrawlerInit):
    def __init__(self, api_key=None, api_path="https://async.scraperapi.com/jobs"):
        self.api_key = self.__set_api_key(api_key)
        self.rs = requests.session()
        self.api_path = api_path
        self.job_status_url = None
        self.job_status = False

        self.runtime_status = False
        self.runtime_response = None

    class JobStatus(str, Enum):
        Running = "running"
        Finished = "finished"

    @dataclasses.dataclass
    class JobTask:
        status: bool
        response: Any

    def __set_api_key(self, api_key):
        if api_key is None:
            raise ValueError
        return api_key

    def get_page(self, url, render=True, headers=None):
        payload = {
            "apiKey": self.api_key,
            "url": url,
            "render": render,
            "method": "GET",
        }
        if headers is not None:
            payload["headers"] = headers

        qaq = self.rs.post(self.api_path, json=payload)
        created = qaq.json()
        self.job_status = created.get("status")
        self.job_status_url = created.get("statusUrl")

        return self

    def get_status(self) -> JobTask:
        if not self.runtime_status:
            job_response = self.rs.get(self.job_status_url).json()
            self.job_status = job_response.get("status")

            if self.job_status == self.JobStatus.Finished:
                self.runtime_status = True
                self.runtime_response = job_response.get("response").get("body")

        return self.JobTask(status=self.runtime_status, response=self.runtime_response)

    def get_response(self, sleep_secs=20):
        while True:
            runtime_tasks = self.get_status()
            if runtime_tasks.status:
                break
            else:
                print(f"{runtime_tasks.status =} wait {sleep_secs}...")
                time.sleep(sleep_secs)

        return runtime_tasks.response


if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
    this_env = ROOT_DIR / ".env"
    if this_env.exists():
        load_dotenv(this_env)
    SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY", None)

    asc = ScraperAsyncApiCrawler(api_key=SCRAPER_API_KEY)
    target_url = (
        "https://www.kkday.com/zh-tw/product/ajax_productlist/A01-001?"
        "city=&"
        "row=50&"
        "glang=&"
        "cat=TAG_3&"
        "availstartdate=&"
        "availenddate=&"
        "fprice=&"
        "eprice=&"
        "sort=prec&"
        "page=1"
    )
    r = asc.get_page(target_url).get_response()
    print(r)
