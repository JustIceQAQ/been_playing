import pathlib

from bs4 import BeautifulSoup

from helpers.translation.base import TranslationInit


class BeautifulSoupTranslation(TranslationInit):
    def translation_to_object(
        self, text: str | None, format_encoding: str | None = "html5lib", *args, **kwargs
    ) -> BeautifulSoup | None:
        if text is None:
            return None
        return BeautifulSoup(text, format_encoding)

    def load_file_to_object(self, file: pathlib.Path, format_encoding: str | None = "html5lib") -> BeautifulSoup:
        return BeautifulSoup(file.read_text(encoding="utf-8"), format_encoding)
