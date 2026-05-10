import asyncio
from typing import cast

from app.museums.ioesinica.parse import IOESinicaParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan

from helpers.utils_helper import month_3

from helpers.crawler.niquests.helper import NiquestsAsyncSession

from selectolax.lexbor import LexborNode
from helpers.translation.selectolax import SelectolaxTranslation


class IOESinicaRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = IOESinicaParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.nangang_63000090,
            fullname="中央研究院-民族學研究所博物館",
            code_name="IOESinica",
            external_link="https://www.ioe.sinica.edu.tw/",
            branch_coordinates=Coordinate(raw_coordinates="25.039370042568287, 121.61723912563318"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="www.ioe.sinica.edu.tw")
        async with NiquestsAsyncSession(headers=headers) as client:
            params = {
                "filter": "352FF7AE-29BF-4A29-B877-C871A001856C",
                "Catefilter": "1DE93031-F3C8-4AA0-94D8-EAD4BABD62BA",
                "SiteID": "416763f8-a1f7-48fd-bfbf-9327913efad7",
            }
            response = await client.get("https://www.ioe.sinica.edu.tw/ExhibitionCurrent/List", params=params)
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        return parsed.css("div.museum_ic_list_block a")


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image.none.helper import NoneImage

    await IOESinicaRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
