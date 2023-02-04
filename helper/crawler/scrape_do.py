from enum import Enum
from urllib.parse import urlencode

import requests

from helper.crawler import CrawlerInit


class ScrapeDoCrawler(CrawlerInit):
    class Formatted(str, Enum):
        text = "text"
        json = "json"

    def __init__(self, token=None, api_url="http://api.scrape.do"):
        self.token = token
        self.api_url = api_url

    def get_page(self, url, formatted="text"):
        full_url = urlencode({"token": self.token, "url": url})
        response = requests.get(f"{self.api_url}?{full_url}")

        if formatted in {self.Formatted.text}:
            return response.text
        elif formatted in {self.Formatted.json}:
            return response.json()


if __name__ == "__main__":
    dd = ScrapeDoCrawler(token="d0ba7028c1604b21b8bdae1076703b1d5d60408511f")
    ok = dd.get_page(url="https://www.klook.com/zh-TW/event/19-taipei/")
    print(ok)
