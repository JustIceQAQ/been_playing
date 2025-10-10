import asyncio
import datetime
import uuid
from typing import Any

from app.exhibition.pier2.parse import Pier2Parse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class Pier2Runner(RunnerInit):
    translation = JsonTranslation
    use_parse = Pier2Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="駁2藝術特區",
            code_name="Pier2",
            external_link="https://pier2.org/exhibition/list/all/",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://pier2.org/exhibition/list/all/",
            "origin": "https://pier2.org",
        }
        cookies = {"PHPSESSID": uuid.uuid4().hex}
        params = {
            "type": "exhibition",
            "date": f"{datetime.date.today():%Y-%m-%d}",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post(
                "https://pier2.org/api/eventList.php", params=params, cookies=cookies
            )
        return response.json()

    async def fetch_parsed(self):
        parsed: dict[str, Any] = await super().fetch_parsed()
        return parsed.get("list", [])


async def main():
    await Pier2Runner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
