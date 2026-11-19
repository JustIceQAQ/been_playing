import abc
import inspect
from typing import Any

from helpers.storage.helper import ExhibitionItem

Values = str | list[Any] | None


class ParseInit(abc.ABC):
    @abc.abstractmethod
    def get_title(self, *args, **kwargs) -> str | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_date(self, *args, **kwargs) -> str | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_address(self, *args, **kwargs) -> str | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_figure(self, *args, **kwargs) -> str | None:
        raise NotImplementedError

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        return None

    @abc.abstractmethod
    def get_source_url(self, *args, **kwargs) -> str | None:
        raise NotImplementedError

    def parsed(self, *args, **kwargs) -> dict[str, Any]:
        methods = [
            method for method in inspect.getmembers(self, predicate=inspect.ismethod) if method[0].startswith("get_")
        ]
        return {def_name.split("get_")[-1]: method(*args, **kwargs) for def_name, method in methods}

    def parse_to_base_model(self, base_model: type[ExhibitionItem], *args, **kwargs) -> ExhibitionItem:
        parsed_data = self.parsed(*args, **kwargs)
        clean_data = {key: self.clean_string(value) for key, value in parsed_data.items()}

        return base_model.model_validate(clean_data)

    def clean_string(self, raw_values: Values) -> Values:
        replace_string_set = {"日期：", " more", "地點："}
        if raw_values is None:
            return None
        if isinstance(raw_values, list):
            return [self.clean_string(raw_value) for raw_value in raw_values]
        for replace_string in replace_string_set:
            raw_values = raw_values.replace(replace_string, " ")
        return " ".join(raw_values.split()).strip()
