import asyncio
import base64
import json
import secrets
from typing import cast

import bs4
import httpx

from app.museums.tmc.parse import TmcParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class TmcRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TmcParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.nangang_63000090,
            fullname="台北流行音樂中心",
            code_name="Tmc",
            external_link="https://www.tmc.taipei/tw/blog/show?filter=eyJkaXJlY3Rpb24iOiJsYXN0ZXN0In0=",
            branch_coordinates=Coordinate(raw_coordinates="25.05181188396233, 121.59745382637806"),
            venue_type=VenueType.EXPO_CENTER,
        )

    def create_filter_base64_string(self, page_number: int) -> str:
        str_dict = json.dumps(
            {
                "pages": page_number,
                "category": "",
                "year": "",
                "month": "",
                "keyword": "",
                "direction": "latest",
            }
        )
        return base64.b64encode(str_dict.encode()).decode()

    async def fetch_response(self):
        headers = generate_headers(
            host="www.tmc.taipei",
            other_headers={
                "accept": "text/html,"
                "application/xhtml+xml,"
                "application/xml;q=0.9,"
                "image/avif,"
                "image/webp,"
                "image/apng,*/*;q=0.8,"
                "application/signed-exchange;v=b3;q=0.7",
            },
        )
        cookie_jar = httpx.Cookies()
        cookie_jar.set("ci_session", secrets.token_hex(8), domain="www.tmc.taipei")
        target_url = "https://www.tmc.taipei/tw/blog/show"
        responses_text = []
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(
                target_url,
                params={"filter": self.create_filter_base64_string(1)},
                cookies=cookie_jar,
            )
            response.raise_for_status()
            responses_text.append(response.text)
            pagination_len = (
                len(self.translation().translation_to_object(response.text).select("li.c-pagination-item")) - 2
            )
            if pagination_len != 1:
                for n in range(2, pagination_len + 1):
                    sub_response = await client.get(
                        target_url,
                        params={"filter": self.create_filter_base64_string(n)},
                        cookies=cookie_jar,
                    )
                    sub_response.raise_for_status()
                    responses_text.append(sub_response.text)

        return responses_text

    async def fetch_parsed(self):
        items = []
        parsers = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        for parsed in parsers:
            items.extend(parsed.select(".card-section > div.card-wrap > a.c-card-clip-wrap"))
        return items


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await TmcRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
