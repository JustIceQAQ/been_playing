SCRIPT_CODE = """from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.utils_helper import month_3


class {script_code}Runner(RunnerInit):
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
        pass



if __name__ == '__main__':
    {script_code}Runner().run()
"""


PARSE_CODE = """
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
