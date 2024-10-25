from bs4 import BeautifulSoup

from helpers.translation.base import TranslationInit


class BeautifulSoupTranslation(TranslationInit):
    def translation_to_object(
        self, text: str, format_encoding: str | None = "html5lib", *args, **kwargs
    ) -> BeautifulSoup:
        return BeautifulSoup(text, format_encoding)
