import abc
import inspect
from typing import Any

import bs4
from pydantic import BaseModel


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

    def parse_to_base_model(self, base_model: BaseModel, *args, **kwargs) -> BaseModel:
        parsed_data = self.parsed(*args, **kwargs)
        return base_model.model_validate(parsed_data)
