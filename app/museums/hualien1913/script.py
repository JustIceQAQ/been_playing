import asyncio

from typing import cast, TYPE_CHECKING
from app.museums.hualien1913.parse import HuaLien1913Parse
from app.museums.hualien1913.information import HuaLien1913Information
from app.museums.hualien1913.social_media import HuaLien1913SocialMedia
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.utils_helper import month_3, get_date


from helpers.crawler.niquests.helper import NiquestsAsyncSession


from selectolax.lexbor import LexborNode
from helpers.translation.selectolax import SelectolaxTranslation


if TYPE_CHECKING:
    from helpers.storage.helper import Information
    from helpers.storage.social_media import SocialMedia


class HuaLien1913Runner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = HuaLien1913Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return HuaLien1913Information.get_information()

    def set_social_media(self) -> "SocialMedia":
        return HuaLien1913SocialMedia.get_social_media()

    async def fetch_response(self):
        headers = generate_headers()
        async with NiquestsAsyncSession(headers=headers) as client:
            response = await client.get("https://hualien1913.nat.gov.tw/%E6%9C%80%E6%96%B0%E6%B4%BB%E5%8B%95/")
        return response.text

    async def fetch_parsed(self):
        this_year = get_date.now_year
        parsed = cast(LexborNode, await super().fetch_parsed())
        items = parsed.css(f"div.grid-items div.item.exhibition.ud{this_year}")
        return items


async def main():
    from helpers.cache import none_cache
    from helpers.image_hosting import none_image_hosting

    await HuaLien1913Runner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
