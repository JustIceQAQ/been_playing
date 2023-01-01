import inspect
from abc import ABCMeta, abstractmethod
from typing import Any, Dict

import bs4


class ParseInit(metaclass=ABCMeta):
    @abstractmethod
    def get_title(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_date(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_address(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_figure(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_source_url(self, *args, **kwargs) -> str:
        raise NotImplementedError

    def parsed(self, *args, **kwargs) -> Dict[str, Any]:
        methods = [
            method
            for method in inspect.getmembers(self, predicate=inspect.ismethod)
            if method[0].startswith("get_")
        ]
        return {
            def_name.split("get_")[-1]: method(*args, **kwargs)
            for def_name, method in methods
        }


class TWTCParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item
        self.item_tds = item.select("td")

    def get_title(self, *args, **kwargs) -> str:
        return self.item_tds[1].get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item_tds[0].get_text()

    def get_address(self, *args, **kwargs) -> str:
        return self.item_tds[4].get_text()

    def get_figure(self, *args, **kwargs) -> str:
        return ""

    def get_source_url(self, *args, **kwargs) -> str:
        nth_child_a = self.item_tds[1].select("a")
        if len(nth_child_a) > 1:
            return nth_child_a[0].get("href", None)
        else:
            return "https://twtc.com.tw/" + nth_child_a[0].get("href", None)
