import asyncio
import secrets

from app.exhibition.ocam.parse import OCAMParse
from helpers.cache.none import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class OCAMRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = OCAMParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="陽明海洋文化藝術館",
            code_name="OCAM",
            external_link="https://www.ocam.org.tw/tw/Exhibition/OCAM",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "host": "www.ocam.org.tw",
            "origin": "https://www.ocam.org.tw",
            "referer": "https://www.ocam.org.tw/tw/Exhibition/OCAM",
            "x-requested-with": "XMLHttpRequest",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "priority": "u=1, i",
        }
        cookies = {"CONSENT": "YES+", "PHPSESSID": secrets.token_hex(16)}
        data = {"site": "OCAM", "nowpage": 1, "ispast": 0}
        url = "https://www.ocam.org.tw/tw/Exhibition/NowPage"
        datas = []
        async with HttpxAsyncClient(headers=headers, cookies=cookies) as client:
            while True:
                response = await client.post(url, data=data)
                response.raise_for_status()
                raw_data = response.json()
                datas.extend(raw_data["data"])
                last_page = raw_data["page"]["p"]["last"]
                if last_page == data["nowpage"]:
                    break
                data["nowpage"] += 1
        return datas

    async def fetch_parsed(self):
        parsed: list[dict] = await super().fetch_parsed()
        return parsed


async def main():
    await OCAMRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
