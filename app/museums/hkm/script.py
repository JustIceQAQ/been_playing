import asyncio
from typing import cast

from app.museums.hkm.parse import HKMParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan

from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage

from helpers.crawler.niquests.helper import NiquestsAsyncSession

from selectolax.lexbor import LexborNode
from helpers.translation.selectolax import SelectolaxTranslation


class HKMRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = HKMParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.shilin_63000110,
            fullname="華岡博物館",
            code_name="hkm",
            external_link="https://hkm.pccu.edu.tw/",
            branch_coordinates=Coordinate(raw_coordinates="25.13827980838548, 121.54058154232688"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(referer="https://hkm.pccu.edu.tw/")
        async with NiquestsAsyncSession(headers=headers) as client:
            urls = [
                "https://hkm.pccu.edu.tw/exhibition/exhibition-preview",
                "https://hkm.pccu.edu.tw/exhibition/current-exhibition",
            ]
            responses = await asyncio.gather(*[client.get(url) for url in urls])

        return [response.text for response in responses]

    async def fetch_parsed(self):
        parsed = cast(list[LexborNode], await super().fetch_parsed())
        items = []
        for p in parsed:
            items.extend(p.css("div.view-content > div.views-row > div"))
        return items


async def main():
    await HKMRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
