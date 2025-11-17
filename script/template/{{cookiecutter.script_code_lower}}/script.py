import asyncio

import bs4
from app.{{cookiecutter.target_sub_directory}}.{{cookiecutter.script_code_lower}}.parse import {{cookiecutter.script_code}}Parse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class {{cookiecutter.script_code}}Runner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = {{cookiecutter.script_code}}Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="",
            code_name="",
            external_link=""
        )

    async def fetch_response(self):
        headers = dict(**get_header())
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get()
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()



async def main():
    await {{cookiecutter.script_code}}Runner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())