import asyncio

from typing import cast
from app.{{cookiecutter.target_sub_directory}}.{{cookiecutter.script_code_lower}}.parse import {{cookiecutter.script_code}}Parse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient

from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage

{% set venue_type = "" %}
{% if cookiecutter.target_sub_directory == "museums" %}
    {% set venue_type = "VenueType.MUSEUM" %}
{% elif cookiecutter.target_sub_directory == "galleries" %}
    {% set venue_type = "VenueType.GALLERY" %}
{% elif cookiecutter.target_sub_directory == "platform" %}
    {% set venue_type = "VenueType.PLATFORM" %}
{% endif %}



{%  set crawler_fetch_type = "" %}
{% if cookiecutter.crawler == "niquests" %}
from helpers.crawler.niquests.helper import NiquestsAsyncSession
{% set crawler_fetch_type = "NiquestsAsyncSession" %}
{% elif cookiecutter.crawler == "httpx" %}
from helpers.crawler.httpx.helper import HttpxAsyncClient
{% set crawler_fetch_type = "HttpxAsyncClient" %}
{% endif %}





{% set translation_type = "" %}
{% set fetch_parsed_return_type = "" %}

{% if cookiecutter.translation == "Selectolax" %}
from selectolax.lexbor import LexborNode
from helpers.translation.selectolax import SelectolaxTranslation
{% set translation_type = "SelectolaxTranslation" %}
{% set fetch_parsed_return_type = "LexborNode" %}

{% elif cookiecutter.translation == "BeautifulSoup4" %}
from bs4 import BeautifulSoup
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
    {% set translation_type = "BeautifulSoupTranslation" %}
    {% set fetch_parsed_return_type = "BeautifulSoup" %}
{% elif cookiecutter.translation == "Json" %}
from helpers.translation.json import JsonTranslation
    {% set translation_type = "JsonTranslation" %}
    {% set fetch_parsed_return_type = "dict" %}
{% endif %}


class {{cookiecutter.script_code}}Runner(RunnerInit):
    translation = {{ translation_type }}
    use_parse = {{cookiecutter.script_code}}Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        {% if cookiecutter.target_sub_directory == "platform" %}
        return Information(
            fullname="",
            code_name="",
            external_link="",
            venue_type={{venue_type}},
        )
        {% else %}
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="",
            code_name="",
            external_link="",
            branch_coordinates=Coordinate(raw_coordinates=None),
            venue_type={{venue_type}},
        )
        {% endif %}




    async def fetch_response(self):
        headers = generate_headers()
        async with {{ crawler_fetch_type }}(headers=headers) as client:
            response = await client.get()
        return response.text

    async def fetch_parsed(self):
        parsed = cast({{fetch_parsed_return_type}}, await super().fetch_parsed())



async def main():
    await {{cookiecutter.script_code}}Runner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())