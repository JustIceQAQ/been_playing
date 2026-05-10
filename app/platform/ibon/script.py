import asyncio

from app.platform.ibon.parse import IBonParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.symbol.venue import VenueType
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class IBonRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = IBonParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="IBon 售票",
            code_name="IBon",
            external_link="https://tour.ibon.com.tw/home/search?category=exhibition",
            venue_type=VenueType.PLATFORM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        headers["Referer"] = "https://tour.ibon.com.tw/home/search?category=exhibition"

        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                "https://tour.ibon.com.tw/api/public/event/list?page=1&limit=100&category=5fe4480d3ff56763f1bb99ba",
            )
        return response.json()

    async def fetch_parsed(self) -> list[dict]:
        result = await super().fetch_parsed()
        if isinstance(result, dict):
            return result.get("list", [])
        return []


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await IBonRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
