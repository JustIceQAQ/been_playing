import asyncio
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.tam.parse import TAMParse
from helpers.cache.none.helper import NoneCache
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Coordinate, Information
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3


class TAMRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = TAMParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taitung.tai_dong_10014010,
            fullname="臺東美術館",
            code_name="TAM",
            external_link="https://tm.ccl.ttct.edu.tw/",
            branch_coordinates=Coordinate(raw_coordinates="22.764445563601402, 121.14989120697749"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        appsname = ["ExhibitionsList4102", "ExhibitionsList4101"]
        async with NiquestsAsyncSession(headers=headers) as client:
            responses = await asyncio.gather(
                *[
                    client.get("https://tm.ccl.ttct.edu.tw/ExhibitionsListC004100.php", params={"appname": appname})
                    for appname in appsname
                ]
            )
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parsed = cast(list[LexborNode], await super().fetch_parsed())
        items = []
        for p in parsed:
            items.extend(p.css("div.kf_cardlist div.kf_imglist a"))
        return items


async def main():
    await TAMRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
