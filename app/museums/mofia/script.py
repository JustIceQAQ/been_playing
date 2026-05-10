import asyncio
from typing import cast

from app.museums.mofia.parse import MofiaParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class MofiaRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = MofiaParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taichung.dali_66000280,
            fullname="臺中市纖維工藝博物館",
            code_name="Mofia",
            external_link="https://mofia.taichung.gov.tw/",
            branch_coordinates=Coordinate(raw_coordinates="24.100248374856758, 120.68606998009467"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post(
                "https://mofia.taichung.gov.tw/Exhibit/InitExhibit",
                json={"lang": "1", "type": "Current"},
            )
        return response.json()

    async def fetch_parsed(self):
        parsed = cast(dict, await super().fetch_parsed())
        return parsed.get("data")


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImage

    await MofiaRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
