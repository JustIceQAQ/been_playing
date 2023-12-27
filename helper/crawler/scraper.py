import dataclasses
import time
from enum import Enum
from typing import Any, Optional

import requests

from helper.crawler import CrawlerInit


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

        self.runtime_status: Optional[bool] = False
        self.runtime_response = None

    class JobStatus(str, Enum):
        Running = "running"
        Finished = "finished"

    @dataclasses.dataclass
    class JobTask:
        status: Optional[bool]
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
        if self.runtime_status is False:
            job_response = self.rs.get(self.job_status_url)
            if not job_response.ok:
                return self.JobTask(status=None, response={})

            job_result = job_response.json()
            self.job_status = job_result.get("status")

            if self.job_status == self.JobStatus.Finished:
                self.runtime_status = True
                self.runtime_response = job_result.get("response").get("body")

        return self.JobTask(status=self.runtime_status, response=self.runtime_response)

    def get_response(self, sleep_secs=20, tries_flag=5):
        runtime_flag = 0
        while True:
            if runtime_flag != tries_flag:
                runtime_tasks = self.get_status()
                if runtime_tasks.status:
                    runtime_return = runtime_tasks.response
                    break
                elif runtime_tasks.status is None:
                    runtime_return = {}
                    break
                else:
                    runtime_flag += 1
                    print(f"{runtime_tasks.status =} wait {sleep_secs}...")
                    time.sleep(sleep_secs)
            else:
                runtime_return = {}
                break

        return runtime_return
