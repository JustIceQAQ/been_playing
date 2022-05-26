from abc import ABCMeta, abstractmethod
from typing import Dict

from bs4 import BeautifulSoup

from helper.crawler_helper import PyCurlCrawler, RequestsCrawler
from helper.translation_helper import BeautifulSoupTranslation, JsonTranslation

# 爬蟲 + 轉譯器 組合


class InstantiationInit(metaclass=ABCMeta):
    @abstractmethod
    def fetch(self, *args, **kwargs):
        raise NotImplementedError


class RequestsBeautifulSoupInstantiation(
    InstantiationInit, RequestsCrawler, BeautifulSoupTranslation
):
    def fetch(self) -> BeautifulSoup:
        context = self.get_page()
        translation_object = self.format_to_object(context)
        return translation_object


class RequestsJsonInstantiation(InstantiationInit, RequestsCrawler, JsonTranslation):
    def fetch(self, *args, **kwargs) -> Dict:
        context = self.get_page(*args, **kwargs)
        translation_object = self.format_to_object(context)
        return translation_object


class PyCurlBeautifulSoupInstantiation(
    InstantiationInit, PyCurlCrawler, BeautifulSoupTranslation
):
    def fetch(self) -> BeautifulSoup:
        context = self.get_page()
        translation_object = self.format_to_object(context)
        return translation_object
