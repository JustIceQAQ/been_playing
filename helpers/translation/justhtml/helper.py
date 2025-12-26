import pathlib

from justhtml import JustHTML

from helpers.translation.base import TranslationInit


class JustHTMLTranslation(TranslationInit):
    def translation_to_object(self, text: str, *args, **kwargs) -> JustHTML:
        return JustHTML(text, *args, **kwargs)

    def load_file_to_object(self, file: pathlib.Path) -> JustHTML:
        return JustHTML(file.read_text(encoding="utf-8"))
