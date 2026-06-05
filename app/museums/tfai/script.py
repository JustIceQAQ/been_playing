import asyncio

from typing import cast, TYPE_CHECKING

from wreq import Proxy
from app.museums.tfai.parse import TFAIParse
from app.museums.tfai.information import TFAIInformation
from configs.settings import get_settings
from helpers.crawler.wreq.helper import WReqAsyncClient
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.utils_helper import month_3


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

        runtime_settings = get_settings()
        proxies = None if runtime_settings.PROXY_POOL is None else [Proxy.all(runtime_settings.PROXY_POOL)]

        async with WReqAsyncClient(
            headers=headers,
            follow_redirects=True,
            proxies=proxies,
        ) as client:
            response = await client.get(
                "https://www.tfai.org.tw/program/searchAjax?date=&type=Exhibition&location=&topic=",
                cookies=cookies,
            )
        data = await response.json()
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
