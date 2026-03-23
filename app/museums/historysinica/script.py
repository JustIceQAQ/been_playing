import asyncio
import secrets
from typing import cast

from app.museums.historysinica.parse import HistorySinicaParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType

from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage

from helpers.crawler.niquests.helper import NiquestsAsyncSession

from selectolax.lexbor import LexborNode
from helpers.translation.selectolax import SelectolaxTranslation


class HistorySinicaRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = HistorySinicaParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.TAIPEI_CITY,
            fullname="中央研究院-歷史文物陳列館",
            code_name="HistorySinica",
            external_link="https://museum.sinica.edu.tw/",
            branch_coordinates=Coordinate(raw_coordinates="25.03963971275805, 121.61615175259622"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="museum.sinica.edu.tw")
        cookies = generate_cookies(other_cookies={"__Secure-PHPSESSID": secrets.token_hex(13)})
        async with NiquestsAsyncSession(headers=headers) as client:
            response = await client.get("https://museum.sinica.edu.tw/exhibitions-events/", cookies=cookies)
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        items = parsed.css("#main-content div.block-list div.item")
        return items


async def main():
    await HistorySinicaRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
