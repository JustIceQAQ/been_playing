import asyncio
import secrets

from app.exhibition.tfam.parse import TFamParse
from helpers.cache.none import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class TFamRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = TFamParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="臺北市立美術館",
            code_name="TFam",
            external_link="https://www.tfam.museum/Exhibition/Exhibition.aspx?ddlLang=zh-tw",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "Referer": "https://www.tfam.museum/Exhibition/Exhibition.aspx?ddlLang=zh-tw",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "www.tfam.museum",
            "origin": "https://www.tfam.museum",
            "X-Requested-With": "XMLHttpRequest",
            "cookie": f"ASP.NET_SessionId={secrets.token_hex(12)}",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [
                client.post(
                    "https://www.tfam.museum/ashx/Exhibition.ashx?ddlLang=zh-tw",
                    json={"JJMethod": "GetEx", "Type": str(i)},
                )
                for i in range(1, 3)
            ]
            responses = await asyncio.gather(*tasks)
        return [response.json() for response in responses]

    async def fetch_parsed(self):
        data = []
        parsers: list[dict] = await super().fetch_parsed()
        for parsed in parsers:
            data.extend(parsed.get("Data", []))
        return data

    async def fetch_items(self, *args, **kwargs):
        return await super().fetch_items(target_domain="https://www.tfam.museum")


async def main():
    await TFamRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
