import asyncio
import urllib.parse
from .parse import PactParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class PactRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = PactParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="台北偶戲館",
            code_name="PACT",
            external_link="https://www.pact.taipei/exhibition_list.aspx?p=1&ps=10&t=all",
        )

    async def fetch_response(self):
        aspx = "https://www.pact.taipei/exhibition_list.aspx"
        headers = {
            **get_header(),
            "x-requested-with": "XMLHttpRequest",
            "referer": f"{aspx}?p=1&ps=10&t=all",
            "origin": "https://www.pact.taipei",
            "host": "www.pact.taipei",
        }
        data = {
            "q": "get",
            "r": "0.9",
            "t": "all",
            "data": urllib.parse.quote('{"p":1,"ps":10,"t":"all"}'),
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post(aspx, data=data)
            response.raise_for_status()
        return response.json()

    async def fetch_parsed(self):
        parsed: dict = await super().fetch_parsed()
        return parsed["list"]["items"]


async def main():
    await PactRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
