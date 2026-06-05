import asyncio

from typing import cast, TYPE_CHECKING
from app.museums.tfai.parse import TFAIParse
from app.museums.tfai.information import TFAIInformation
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.utils_helper import month_3


from helpers.crawler.niquests.helper import NiquestsAsyncSession


from helpers.translation.json import JsonTranslation


if TYPE_CHECKING:
    from helpers.storage.helper import Information


class TFAIRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = TFAIParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return TFAIInformation.get_information()

    async def fetch_response(self):
        headers = generate_headers(
            x_requested_with="XMLHttpRequest",
            referer="https://www.tfai.org.tw/",
        )
        cookies = generate_cookies(need_js_ession_id=True)
        async with NiquestsAsyncSession(headers=headers) as client:
            response = await client.get(
                "https://www.tfai.org.tw/program/searchAjax?date=&type=Exhibition&location=&topic=",
                cookies=cookies,
            )
            response.raise_for_status()
        data = response.json()
        print(
            f"[TFAI] status={response.status_code}, data keys={list(data.keys()) if isinstance(data, dict) else type(data)}",
            flush=True,
        )
        return data

    async def fetch_parsed(self):
        parsed = cast(dict, await super().fetch_parsed())
        return parsed.get("data", [])


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await TFAIRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
