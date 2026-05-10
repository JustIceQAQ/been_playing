import asyncio
from typing import cast

from app.museums.tcam.parse import TcamParse
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Coordinate, Information
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class TcamRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = TcamParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taichung.xitun_66000060,
            fullname="臺中市立美術館",
            code_name="Tcam",
            external_link="https://www.tcam.museum/",
            branch_coordinates=Coordinate(raw_coordinates="24.193055105364973, 120.65443027094344"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        categories = [
            "upcoming",
            "current",
        ]
        async with NiquestsAsyncSession(headers=headers) as client:
            responses = await asyncio.gather(
                *[
                    client.get(
                        "https://www.tcam.museum/wp-json/api/exhibition-post"
                        f"?lang=zh&sort={category}&categories=exhibition-type&page=1&posts_per_page=10"
                    )
                    for category in categories
                ]
            )
        return [response.json() for response in responses]

    async def fetch_parsed(self):
        parsed = cast(list[dict], await super().fetch_parsed())
        items = []
        for p in parsed:
            items.extend(p.get("data", {}).get("posts", []))
        return items


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image.none.helper import NoneImage

    await TcamRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
