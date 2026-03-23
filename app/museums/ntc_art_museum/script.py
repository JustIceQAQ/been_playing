import asyncio
from typing import cast

import httpx

from app.museums.ntc_art_museum.parse import NtcArtMuseumParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class NtcArtMuseumRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = NtcArtMuseumParse
    use_suffix_item_from_url_auto = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.new_taipei_city,
            fullname="新北市美術館",
            code_name="NtcArtMuseum",
            external_link="https://ntcart.museum/exhibition.aspx?kind=today",
            branch_coordinates=Coordinate(raw_coordinates="24.953654641948525, 121.358269212097"),
            venue_type=VenueType.MUSEUM,
        )

    async def sub_fetch_response(self, client: httpx.AsyncClient, kind: str) -> httpx.Response:
        return await client.post(
            "https://ntcart.museum/exhibition.aspx",
            data={
                "q": "get",
                "r": "0.9999999999999999",
                "data": {"p": 1, "ps": 12, "Kind": kind},
            },
        )

    async def fetch_response(self):
        headers = generate_headers(
            referer="https://ntcart.museum/exhibition.aspx?kind=today",
            origin="https://ntcart.museum",
            x_requested_with="XMLHttpRequest",
            other_headers={"content-type": "application/x-www-form-urlencoded; charset=UTF-8"},
        )
        kinds = [
            "today",
            "future",
        ]
        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [self.sub_fetch_response(client, kind) for kind in kinds]
            responses = await asyncio.gather(*tasks)
        return [response.json() for response in responses]

    async def fetch_parsed(self):
        parsed = cast(list[dict], await super().fetch_parsed())
        all_items = []
        for parse in parsed:
            parse_list = parse.get("list")
            if parse_list is None:
                continue
            this_items = parse_list.get("items")
            if this_items:
                all_items.extend(this_items)
        return all_items


async def main():
    await NtcArtMuseumRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
