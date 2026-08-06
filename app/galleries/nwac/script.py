import asyncio
from typing import TYPE_CHECKING, cast

from selectolax.lexbor import LexborNode

from app.galleries.nwac.information import NWACInformation
from app.galleries.nwac.parse import NWACParse
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.runner.helper import RunnerInit
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3

if TYPE_CHECKING:
    from helpers.storage.helper import Information


class NWACRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = NWACParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return NWACInformation.get_information()

    async def fetch_response(self):
        headers = generate_headers(referer="https://www.nwac.org.tw/tw/appreciate-art/78feae0b7b7489db291861a7f9129bcc")
        async with NiquestsAsyncSession(headers=headers) as client:
            response = await client.get("https://www.nwac.org.tw/tw/appreciate-art")
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        return parsed.css("main.pages-body div.article-list div.article-list__item")[:5]


async def main():
    from helpers.cache import none_cache
    from helpers.image_hosting import none_image_hosting

    await NWACRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
