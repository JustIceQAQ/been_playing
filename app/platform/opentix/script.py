import asyncio

from app.platform.opentix.parse import OpenTixParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class OpenTixRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = OpenTixParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="兩廳院生活文化",
            code_name="OpenTix",
            external_link="https://www.opentix.life/search/%20/ABOUT_TO_BEGIN"
            "?category=%E5%B1%95%E8%A6%BDAll"
            "&type=programs",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "origin": "https://www.opentix.life",
            "referer": "https://www.opentix.life/",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post(
                "https://search.opentix.life/search",
                json={
                    "highlight": False,
                    "language": "zh-CHT",
                    "categoryFilter": ["展覽-主題展"],
                    "sortBy": "ABOUT_TO_BEGIN",
                },
            )
        return response.json()

    async def fetch_parsed(self) -> list:
        parsed: dict = await super().fetch_parsed()
        return parsed.get("result", {}).get("found", [])

    async def fetch_items(self, *args, **kwargs):
        return await super().fetch_items(
            target_domain="https://www.opentix.life/event/"
        )


async def main():
    await OpenTixRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
