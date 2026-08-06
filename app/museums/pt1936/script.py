import asyncio
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.pt1936.parse import PT1936Parse
from configs.settings import get_settings
from helpers.crawler.headers_helper import generate_cookies, generate_headers
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3


class PT1936Runner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = PT1936Parse
    use_suffix_item_from_url_auto = True

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
            location_code=Taiwan.pingtung.pingtung_10013010,
            fullname="屏菸1936文化基地",
            code_name="PT1936",
            external_link="https://www.cultural.pthg.gov.tw/pt1936/News9.aspx?n=8E5540CA059309A8&CategorySN=3630",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="22.66176638838444, 120.50517003897802"),
                raw_coordinates="22.66176638838444, 120.50517003897802",
            ),
            venue_type=VenueType.CREATIVE_PARK,
        )

    async def _fetch_sub_response(self, client, url: str, cookies: dict | None):
        response = await client.get(url, cookies=cookies)
        return response.text

    async def fetch_response(self):
        headers = generate_headers(
            host="www.cultural.pthg.gov.tw",
        )
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with NiquestsAsyncSession(headers=headers) as client:
            client.proxies.update(self.set_proxies())
            response = await client.get(
                "https://www.cultural.pthg.gov.tw/pt1936/News9.aspx?n=8E5540CA059309A8&CategorySN=3630", cookies=cookies
            )
            response_p = SelectolaxTranslation().translation_to_object(response.text)
            if response_p is None:
                return None
            responses = await asyncio.gather(
                *[
                    self._fetch_sub_response(
                        client, ("https://www.cultural.pthg.gov.tw/pt1936/" + (a.attributes.get("href") or "")), cookies
                    )
                    for a in response_p.css("table#ContentPlaceHolder1_gvIndex tbody tr a")
                ]
            )

        return responses

    async def fetch_parsed(self):
        parsed = cast(list[LexborNode], await super().fetch_parsed())
        return parsed


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await PT1936Runner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
