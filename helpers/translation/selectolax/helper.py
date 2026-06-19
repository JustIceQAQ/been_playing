import pathlib

from selectolax.lexbor import LexborHTMLParser

from helpers.translation.base import TranslationInit


class SelectolaxTranslation(TranslationInit):
    def translation_to_object(self, text: str | None, *args, **kwargs) -> LexborHTMLParser | None:
        if text is None:
            return None
        return LexborHTMLParser(text, *args, **kwargs)

    def load_file_to_object(self, file: pathlib.Path) -> LexborHTMLParser:
        return LexborHTMLParser(file.read_text(encoding="utf-8"))
