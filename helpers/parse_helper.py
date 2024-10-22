import abc
import inspect
from typing import Any

import bs4

from helper.clean_helper import RequestsClean
from helpers.storage.helper import ExhibitionItem


class ParseInit(abc.ABC):
    @abc.abstractmethod
    def get_title(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_date(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_address(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_figure(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_source_url(self, *args, **kwargs) -> str:
        raise NotImplementedError

    def safe_get_text(self, obj: Any):
        if obj is None:
            return None
        if isinstance(obj, bs4.element.Tag):
            return obj.get_text()
        return obj

    def parsed(self, *args, **kwargs) -> dict[str, Any]:
        methods = [
            method
            for method in inspect.getmembers(self, predicate=inspect.ismethod)
            if method[0].startswith("get_")
        ]
        return {
            def_name.split("get_")[-1]: method(*args, **kwargs)
            for def_name, method in methods
        }

    def parse_to_base_model(
        self, base_model: type[ExhibitionItem], *args, **kwargs
    ) -> ExhibitionItem:
        parsed_data = self.parsed(*args, **kwargs)
        clean_data = {
            key: RequestsClean.clean_string(value) for key, value in parsed_data.items()
        }
        return base_model.model_validate(clean_data)
