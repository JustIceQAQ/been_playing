import asyncio
from typing import cast

import bs4
from app.museums.tnammuseum.parse import TnamMuseumParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class TnamMuseumRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TnamMuseumParse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.tainan.west_central_67000370,
            fullname="臺南市美術館",
            code_name="TnamMuseum",
            external_link="https://www.tnam.museum/exhibition/current?page=1",
            branch_coordinates=[
                Coordinate(
                    location_code=Taiwan.tainan.west_central_67000370,
                    name="一館",
                    raw_coordinates="22.99117888093109, 120.20502606285312",
                ),
                Coordinate(
                    location_code=Taiwan.tainan.west_central_67000370,
                    name="二館",
                    raw_coordinates="22.99055275877767, 120.20140904089217",
                ),
            ],
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        responses = []
        async with HttpxAsyncClient(headers=headers) as client:
            for url in [
                "https://www.tnam.museum/exhibition/current",
                "https://www.tnam.museum/exhibition/upcoming",
            ]:
                page = 1
                while True:
                    sub_response = await client.get(url, params={"page": page})
                    sub_soup = bs4.BeautifulSoup(sub_response.text, "html.parser")
                    has_items = sub_soup.select("div.layout-large > figure > a")
                    if has_items:
                        responses.append(sub_response.text)
                        page += 1
                        continue
                    break

        return responses

    async def fetch_parsed(self):
        parseds = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        dataset = []
        for parsed in parseds:
            dataset.extend(parsed.select("div.layout-large > figure > a"))

        return dataset


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image.none.helper import NoneImage

    await TnamMuseumRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
