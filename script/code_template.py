SCRIPT_CODE = """from helpers.runner.helper import RunnerInit3
from helpers.storage.helper import Information


class {script_code}Runner(RunnerInit3):
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

    async def fetch_items(self):
        pass


if __name__ == '__main__':
    {script_code}Runner().run()
"""
