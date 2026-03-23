import asyncio
from typing import cast

import bs4

from app.museums.museumpost.parse import MuseumPostParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class MuseumPostRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = MuseumPostParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="郵政博物館",
            code_name="MuseumPost",
            external_link="https://museum.post.gov.tw/post/Postal_Museum/museum/index.jsp?ID=131&topage=1",
            branch_coordinates=[
                Coordinate(name="本館", raw_coordinates="25.032392367745082, 121.5147638567378"),
                Coordinate(
                    name="臺北館",
                    raw_coordinates="25.047556287891062, 121.51158812126322",
                ),
            ],
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="museum.post.gov.tw", other_headers={"Connection": "keep-alive"})
        cookies = generate_cookies(need_js_ession_id=True)
        async with HttpxAsyncClient(headers=headers) as client:
            target_url = "https://museum.post.gov.tw/post/Postal_Museum/museum/index.jsp?ID=131&topage={to_page}"
            responses = []
            page = 1
            response = await client.get(target_url.format(to_page=page), cookies=cookies)
            while self.translation().translation_to_object(response.text).select("ul.part_list > li"):
                responses.append(response.text)
                page += 1
                response = await client.get(target_url.format(to_page=page), cookies=cookies)

            return responses

    async def fetch_parsed(self):
        parsers = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        items = []
        for parsed in parsers:
            items.extend(parsed.select("ul.part_list > li"))
        return items


async def main():
    await MuseumPostRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
