from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Union

from bs4 import BeautifulSoup

# 實作各種類型轉譯器


class TranslationInit(metaclass=ABCMeta):
    @abstractmethod
    def format_to_object(self, *args, **kwargs) -> Union[BeautifulSoup, Dict[Any, Any]]:
        raise NotImplementedError


class BeautifulSoupTranslation(TranslationInit):
    def format_to_object(
        self, text: str, format_encoding: str = "html5lib"
    ) -> BeautifulSoup:
        formatted_object = BeautifulSoup(text, format_encoding)
        return formatted_object


class JsonTranslation(TranslationInit):
    def format_to_object(self, json_context: Dict[Any, Any]) -> Dict[Any, Any]:
        return json_context
