from typing import Any

from helpers.translation.base import TranslationInit


class JsonTranslation(TranslationInit):
    def translation_to_object(self, text: dict[Any, Any] | None, *args, **kwargs) -> dict[Any, Any] | None:
        if text is None:
            return None
        return text
