

from helpers.parse_helper import ParseInit

{% set item_type = "" %}

{% if cookiecutter.translation == "Selectolax" %}
from selectolax.lexbor import LexborNode
{% set item_type = "LexborNode" %}
{% elif cookiecutter.translation == "BeautifulSoup4" %}
import bs4
    {% set item_type = "bs4.element.Tag" %}
{% elif cookiecutter.translation == "Json" %}
    {% set item_type = "dict" %}
{% endif %}

class {{cookiecutter.script_code}}Parse(ParseInit):
    def __init__(self, item: {{ item_type }}):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        pass

    def get_date(self, *args, **kwargs) -> str | None:
        pass

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        pass

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        pass
