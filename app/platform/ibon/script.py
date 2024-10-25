from typing import Any

from app.platform.ibon.parse import IBonParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
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
        )

    async def fetch_response(self):
        headers = get_header()
        headers["Referer"] = "https://tour.ibon.com.tw/home/search?category=exhibition"

        async with HttpxAsyncClient() as client:
            response = await client.get(
                "https://tour.ibon.com.tw/api/public/event/list?page=1&limit=100&category=5fe4480d3ff56763f1bb99ba",
                headers=headers,
            )
        return response.json()

    async def fetch_parsed(self) -> list[dict[str, Any]]:
        parsed: dict[str, Any] = await super().fetch_parsed()
        return parsed.get("list", [])


if __name__ == "__main__":
    IBonRunner().run()
