import asyncio
import secrets
import string

from typing import cast
from app.museums.hcccart.parse import HcccArtParse
from configs.settings import get_settings
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan

from helpers.utils_helper import month_3

from helpers.crawler.niquests.helper import NiquestsAsyncSession


from selectolax.lexbor import LexborNode
from helpers.translation.selectolax import SelectolaxTranslation


class HcccArtRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = HcccArtParse

    def set_proxies(self):
        runtime_settings = get_settings()
        proxies = None
        if runtime_settings.PROXY_POOL is not None:
            proxies = {
                "http": runtime_settings.PROXY_POOL,
                "https": runtime_settings.PROXY_POOL,
            }
        return proxies

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.hualien.hualien_10015010,
            fullname="花蓮美術館",
            code_name="HcccArt",
            external_link="https://art.hccc.gov.tw/",
            branch_coordinates=Coordinate(raw_coordinates="23.99010271299585, 121.62877324046998"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="art.hccc.gov.tw")
        cookies = {
            "locale": "tw",
            "art": "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(40)),
        }
        async with NiquestsAsyncSession(headers=headers) as client:
            client.proxies.update(self.set_proxies())
            response = await client.get(
                "https://art.hccc.gov.tw/%E5%B1%95%E8%A6%BD/%E7%95%B6%E6%9C%9F%E5%B1%95%E8%A6%BD", cookies=cookies
            )
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        return parsed.css("#content div.ham-card-expo")


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await HcccArtRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
