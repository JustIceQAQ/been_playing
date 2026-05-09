import asyncio
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.pt1936.parse import PT1936Parse
from helpers.cache.none.helper import NoneCache
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_cookies, generate_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Coordinate, Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3


class PT1936Runner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = PT1936Parse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.pingtung.pingtung_10013010,
            fullname="屏菸1936文化基地",
            code_name="PT1936",
            external_link="https://www.cultural.pthg.gov.tw/pt1936/News9.aspx?n=8E5540CA059309A8&CategorySN=3630",
            branch_coordinates=Coordinate(raw_coordinates="22.66176638838444, 120.50517003897802"),
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
            response = await client.get(
                "https://www.cultural.pthg.gov.tw/pt1936/News9.aspx?n=8E5540CA059309A8&CategorySN=3630", cookies=cookies
            )
            response_p = SelectolaxTranslation().translation_to_object(response.text)
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
    await PT1936Runner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
