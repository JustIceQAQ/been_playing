import asyncio
from typing import TYPE_CHECKING, cast


from app.museums.taiwanhistorica.information import TaiwanHistoricaInformation
from app.museums.taiwanhistorica.parse import TaiwanHistoricaParse
from app.museums.taiwanhistorica.social_media import TaiwanHistoricaSocialMedia
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3

if TYPE_CHECKING:
    from helpers.storage.helper import Information
    from helpers.storage.social_media import SocialMedia


class TaiwanHistoricaRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = TaiwanHistoricaParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return TaiwanHistoricaInformation.get_information()

    def set_social_media(self) -> "SocialMedia":
        return TaiwanHistoricaSocialMedia.get_social_media()

    async def fetch_response(self):
        headers = generate_headers(
            referer="https://www.th.gov.tw/",
            origin="https://www.th.gov.tw",
        )
        async with NiquestsAsyncSession(headers=headers) as client:
            response = await client.get(
                "https://api.th.gov.tw/6/News/232?handler=News&Title=&Column001=&Column002=&Column004=&Content=&PageSize=20&PageNumber=1"
            )
        return response.json()

    async def fetch_parsed(self):
        parsed = cast(dict, await super().fetch_parsed())
        return parsed.get("Data")


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await TaiwanHistoricaRunner().run(none_cache, none_image_hosting, develop_mode=True)


if __name__ == "__main__":
    asyncio.run(main())
