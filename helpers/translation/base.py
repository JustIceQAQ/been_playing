import abc
from typing import Any

ObjectType = str | dict[Any, Any] | None


class TranslationInit(abc.ABC):
    @abc.abstractmethod
    def translation_to_object(self, text: ObjectType, *args, **kwargs) -> ObjectType:
        raise NotImplementedError
