SCRIPT_CODE = """import bs4
from app.exhibition.{script_code}.parse import {script_code}Parse
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class {script_code}Runner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = {script_code}Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="",
            code_name="",
            external_link=""
        )

    async def fetch_response(self):
        pass

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()



if __name__ == '__main__':
    {script_code}Runner().run()
"""


PARSE_CODE = """
import bs4

from helpers.parse_helper import ParseInit


class {script_code}Parse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        pass

    def get_date(self, *args, **kwargs) -> str | None:
        pass

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        pass
"""
