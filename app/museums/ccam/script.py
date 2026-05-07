import asyncio
from typing import cast

import niquests
from selectolax.lexbor import LexborNode

from app.museums.ccam.parse import CCAMParse
from helpers.cache.none.helper import NoneCache
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Coordinate, Information
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3


class CCAMRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = CCAMParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.changhua.zhang_hua_10007010,
            fullname="彰化縣立美術館",
            code_name="CCAM",
            external_link="https://fam.bocach.gov.tw/",
            branch_coordinates=Coordinate(raw_coordinates="24.077744219640863, 120.54594898158135"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def _fetch_sub_item_response(self, client: niquests.AsyncSession, url: str, cookies: dict | None):
        response = await client.get(url, cookies=cookies)
        return response.text

    async def _fetch_sub_items_response(
        self, client: niquests.AsyncSession, url: str, cookies: dict | None
    ) -> list[LexborNode]:
        response = await client.get(url, cookies=cookies)
        p = SelectolaxTranslation().translation_to_object(response.text)
        divs = p.css("div.group-list a.div")
        return await asyncio.gather(
            *[
                self._fetch_sub_item_response(
                    client, "https://fam.bocach.gov.tw/" + div.attributes.get("href"), cookies
                )
                for div in divs
            ]
        )

    async def fetch_response(self):
        headers = generate_headers(
            referer="https://fam.bocach.gov.tw/News2.aspx?n=989&sms=10480", host="fam.bocach.gov.tw"
        )
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with NiquestsAsyncSession(headers=headers) as client:
            urls = [
                "https://fam.bocach.gov.tw/News2.aspx?n=990&sms=10480",
                "https://fam.bocach.gov.tw/News2.aspx?n=989&sms=10480",
            ]
            responses = await asyncio.gather(*[self._fetch_sub_items_response(client, url, cookies) for url in urls])
        return [item for sublist in responses for item in sublist]

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        return parsed


async def main():
    await CCAMRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
