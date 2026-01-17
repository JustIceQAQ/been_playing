import asyncio

import bs4

from app.{{cookiecutter.target_sub_directory}}.{{cookiecutter.script_code_lower}}.parse import {{cookiecutter.script_code}}Parse
from helpers.headers_helper import get_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage

{% set v_type = "" %}
{% if cookiecutter.target_sub_directory == "museums" %}
    {% set v_type = "VenueType.MUSEUM" %}
{% elif cookiecutter.target_sub_directory == "galleries" %}
    {% set v_type = "VenueType.GALLERY" %}
{% elif cookiecutter.target_sub_directory == "platform" %}
    {% set v_type = "VenueType.PLATFORM" %}
{% endif %}


class {{cookiecutter.script_code}}Runner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = {{cookiecutter.script_code}}Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        {% if cookiecutter.target_sub_directory == "platform" %}
        return Information(
            fullname="",
            code_name="",
            external_link="",
            venue_type={{v_type}},
        )
        {% else %}
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="",
            code_name="",
            external_link="",
            branch_coordinates=Coordinate(raw_coordinates=None),
            venue_type={{v_type}},
        )
        {% endif %}




    async def fetch_response(self):
        headers = get_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get()
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()



async def main():
    await {{cookiecutter.script_code}}Runner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())