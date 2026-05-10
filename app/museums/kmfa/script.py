import asyncio

import bs4
import httpx

from app.museums.kmfa.parse import KmFaParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3

from typing import cast


class KmFaRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KmFaParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.kaohsiung.gushan_64000020,
            fullname="高雄市立美術館",
            code_name="KmFa",
            external_link="https://www.kmfa.gov.tw/ExhibitionListC001100.aspx?Place=1&SearchDate=1",
            branch_coordinates=Coordinate(raw_coordinates="22.65687499527212, 120.28659401204955"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def sub_response(self, client: httpx.AsyncClient, url: str, *args, **kwargs) -> str:
        response = await client.get(url, *args, **kwargs)
        response.raise_for_status()
        return response.text

    async def fetch_response(self):
        headers = generate_headers(referer="https://www.kmfa.gov.tw/ExhibitionListC001100.aspx?Place=1&SearchDate=1")
        cookies = generate_cookies(need_asp_net_session_id=True, need_consent=True)
        urls = [
            "https://www.kmfa.gov.tw/ExhibitionListC001100.aspx?Place=1&SearchDate=1",
            "https://www.kmfa.gov.tw/ExhibitionListC001100.aspx?Place=1&SearchDate=2",
        ]
        async with HttpxAsyncClient(headers=headers) as client:
            responses = await asyncio.gather(*[self.sub_response(client, url, cookies=cookies) for url in urls])
        return responses

    async def fetch_parsed(self):
        items = []
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        for parse in parsed:
            sub_items = parse.select("div.exhibition_list > a")
            items.extend(sub_items)
        return items


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await KmFaRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
