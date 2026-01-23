import asyncio
from typing import Any

from app.platform.gacc.parse import GaCcParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.storage.symbol import VenueType
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class GaCcRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = GaCcParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="中華文化總會",
            code_name="GaCc",
            external_link="https://www.gacc.org.tw/TW/events?categoryId=3",
            venue_type=VenueType.PLATFORM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            referer="https://www.gacc.org.tw/TW/events?categoryId=3",
            other_headers={
                "content-type": "application/json",
                "content-language": "TW",
            }
        )
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://www.gacc.org.tw/backstage/api/v1/events",
                params={"is_memorial": "0", "is_southern_taipei_event": "0"},
            )
        return response.json()

    async def fetch_parsed(self):
        parsed: dict[str, Any] = await super().fetch_parsed()
        return parsed.get("data").get("data")


async def main():
    await GaCcRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
