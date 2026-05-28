import asyncio
from typing import TYPE_CHECKING, cast

from selectolax.lexbor import LexborNode

from app.museums.xzcac.information import XZCACInformation
from app.museums.xzcac.parse import XZCACParse
from app.museums.xzcac.social_media import XZCACSocialMedia
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3

if TYPE_CHECKING:
    from helpers.storage.helper import Information
    from helpers.storage.social_media import SocialMedia


class XZCACRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = XZCACParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return XZCACInformation.get_information()

    def set_social_media(self) -> "SocialMedia":
        return XZCACSocialMedia.get_social_media()

    async def fetch_response(self):
        headers = generate_headers(host="www.xzcac.ntpc.gov.tw")
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with NiquestsAsyncSession(headers=headers) as client:
            main_response = await client.get(
                "https://www.xzcac.ntpc.gov.tw/xmdoc?xsmsid=0G286646220085905951", cookies=cookies
            )
            main_parse = SelectolaxTranslation().translation_to_object(main_response.text)
            items = main_parse.css("div#PageListContainer div.item a")
            responses = await asyncio.gather(
                *[
                    client.get("https://www.xzcac.ntpc.gov.tw" + item.attributes.get("href"), cookies=cookies)
                    for item in items
                ]
            )

        return [response.text for response in responses]

    async def fetch_parsed(self):
        parsed = cast(list[LexborNode], await super().fetch_parsed())
        return parsed


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await XZCACRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
