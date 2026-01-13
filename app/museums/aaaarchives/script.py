import asyncio
import secrets

from justhtml import JustHTML

from app.museums.aaaarchives.parse import AAAArchivesParse
from helpers.headers_helper import get_headers, get_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.justhtml.helper import JustHTMLTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class AAAArchivesRunner(RunnerInit):
    translation = JustHTMLTranslation
    use_parse = AAAArchivesParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.new_taipei_city,
            fullname="國家發展委員會檔案管理局",
            code_name="AAAArchives",
            external_link="https://aaa.archives.tw/tw/event/306.html",
            branch_coordinates=Coordinate(raw_coordinates="25.07521442685089, 121.37402598256791"),
        )

    async def fetch_response(self):
        url = "https://aaa.archives.tw/tw/event/306.html"
        headers = get_headers(
            referer=url,
            origin="https://aaa.archives.tw",
            host="aaa.archives.tw",
            other_headers={
                "content-type": "application/x-www-form-urlencoded",
            }
        )
        cookies = {
            **get_cookies(need_js_ession_id=True),
            "cookiesession1": secrets.token_hex(16)
        }
        data = {
            "nowPage": 1,
            "pageSize": 60,
        }
        async with HttpxAsyncClient(headers=headers, cookies=cookies, verify=False) as client:
            response = await client.post(url, data=data)
        return response.text

    async def fetch_parsed(self):
        parsed: JustHTML = await super().fetch_parsed()
        li = parsed.query("div.actList > ul > li")
        return li


async def main():
    await AAAArchivesRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
