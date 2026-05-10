import asyncio
import secrets
from typing import cast

from selectolax.lexbor import LexborNode
from app.museums.aaaarchives.parse import AAAArchivesParse
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3


class AAAArchivesRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = AAAArchivesParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.new_taipei.linkou_65000170,
            fullname="國家發展委員會檔案管理局",
            code_name="AAAArchives",
            external_link="https://aaa.archives.tw/tw/event/306.html",
            branch_coordinates=Coordinate(raw_coordinates="25.07521442685089, 121.37402598256791"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        url = "https://aaa.archives.tw/tw/event/306.html"
        headers = generate_headers(
            referer=url,
            origin="https://aaa.archives.tw",
            host="aaa.archives.tw",
            other_headers={
                "content-type": "application/x-www-form-urlencoded",
            },
        )
        cookies = generate_cookies(need_js_ession_id=True, other_cookies={"cookiesession1": secrets.token_hex(16)})
        data = {
            "nowPage": 1,
            "pageSize": 60,
        }
        async with NiquestsAsyncSession(headers=headers) as client:
            client.cookies.update(cookies)
            response = await client.post(url, data=data)
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        li = parsed.css("div.actList > ul > li")
        return li


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image.none.helper import NoneImage

    await AAAArchivesRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
