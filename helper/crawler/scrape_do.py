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
        query_parameters = urlencode({"token": self.token, "url": url, "render": True})
        response = requests.get(f"{self.api_url}?{query_parameters}")

        if formatted in {self.Formatted.text}:
            return response.text
        elif formatted in {self.Formatted.json}:
            return response.json()


if __name__ == "__main__":
    dd = ScrapeDoCrawler(token="")
    ok = dd.get_page(
        url="https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1&type=1"
    )
    print(ok)
