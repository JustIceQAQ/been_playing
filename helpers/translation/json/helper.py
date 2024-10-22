from typing import Any

from helpers.translation.base import TranslationInit


class JsonTranslation(TranslationInit):
    def translation_to_object(self, json_context: dict[Any, Any]) -> dict[Any, Any]:
        return json_context
