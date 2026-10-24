import asyncio
from typing import TYPE_CHECKING, cast

from selectolax.lexbor import LexborNode

from app.museums.judicial.information import JudicialInformation
from app.museums.judicial.parse import JudicialParse
from app.museums.judicial.social_media import JudicialSocialMedia
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.niquests import NiquestsAsyncSession
from helpers.runner.helper import RunnerInit
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3

if TYPE_CHECKING:
    from helpers.storage.helper import Information
    from helpers.storage.social_media import SocialMedia


class JudicialRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = JudicialParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return JudicialInformation.get_information()

    def set_social_media(self) -> "SocialMedia":
        return JudicialSocialMedia.get_social_media()

    async def fetch_response(self):
        headers = generate_headers(referer="https://www.judicial.gov.tw/tw/mp-6.html", host="www.judicial.gov.tw")
        async with NiquestsAsyncSession(headers=headers) as client:
            response = await client.get("https://www.judicial.gov.tw/tw/lp-2441-6.html")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        return parsed.css("div.listAlbum a")


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await JudicialRunner().run(none_cache, none_image_hosting, develop_mode=True)


if __name__ == "__main__":
    asyncio.run(main())
