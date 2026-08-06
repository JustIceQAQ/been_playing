import asyncio
from typing import TYPE_CHECKING, cast

from selectolax.lexbor import LexborNode

from app.museums.fuzhong15.information import FuZhong15Information
from app.museums.fuzhong15.parse import FuZhong15Parse
from app.museums.fuzhong15.social_media import FuZhong15SocialMedia
from helpers.crawler.headers_helper import generate_cookies, generate_headers
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.runner.helper import RunnerInit
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3

if TYPE_CHECKING:
    from helpers.storage.helper import Information
    from helpers.storage.social_media import SocialMedia


class FuZhong15Runner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = FuZhong15Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return FuZhong15Information.get_information()

    def set_social_media(self) -> "SocialMedia":
        return FuZhong15SocialMedia.get_social_media()

    async def fetch_response(self):
        headers = generate_headers(host="www.fuzhong15.ntpc.gov.tw")
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with NiquestsAsyncSession(headers=headers) as client:
            main_response = await client.get(
                "https://www.fuzhong15.ntpc.gov.tw/submenu?usein=2&psid=0G253409950556420467", cookies=cookies
            )
            main_parse = SelectolaxTranslation().translation_to_object(main_response.text)
            if main_parse is None:
                return None
            target_url = main_parse.css_first("a[title='當期特展']").attributes.get("href")
            if target_url is None:
                return None
            response = await client.get(target_url, cookies=cookies)
            if response.url == "https://www.fuzhong15.ntpc.gov.tw/":
                return None

        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode | None, await super().fetch_parsed())
        if parsed is None:
            return []
        return [parsed]


async def main():
    from helpers.cache import none_cache
    from helpers.image_hosting import none_image_hosting

    await FuZhong15Runner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
