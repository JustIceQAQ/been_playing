import asyncio
import secrets
from typing import cast, TYPE_CHECKING

from selectolax.lexbor import LexborNode

from app.museums.aaaarchives.information import AAAArchivesInformation
from app.museums.aaaarchives.parse import AAAArchivesParse
from app.museums.aaaarchives.social_media import AAAArchivesSocialMedia
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3

if TYPE_CHECKING:
    from helpers.storage.helper import Information
    from helpers.storage.social_media import SocialMedia


class AAAArchivesRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = AAAArchivesParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return AAAArchivesInformation.get_information()

    def set_social_media(self) -> "SocialMedia":
        return AAAArchivesSocialMedia.get_social_media()

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
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await AAAArchivesRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
