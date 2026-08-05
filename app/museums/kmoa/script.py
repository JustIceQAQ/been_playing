import asyncio
from typing import cast

import bs4

from app.museums.kmoa.parse import KmoaParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_cookies, generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class KmoaRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KmoaParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.keelung.zhongshan_10017050,
            fullname="基隆美術館",
            code_name="kmoa",
            external_link="https://kmoa.klcg.gov.tw/News_Photo.aspx?n=7484&sms=12489",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.131248388298207, 121.74399937483508"),
                raw_coordinates="25.131248388298207, 121.74399937483508",
            ),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_sub_response(self, client, context: str, *args, **kwargs) -> list[str]:
        p = BeautifulSoupTranslation().translation_to_object(context)
        if p is None:
            return []
        div = p.find("div", {"class": "group-list page-block PhotoList"})
        if div is None:
            return []
        lis = div.find_all("a")
        tasks = [client.get("https://kmoa.klcg.gov.tw/" + a["href"], *args, **kwargs) for a in lis]
        responses = await asyncio.gather(*tasks)
        responses_text = [response.text for response in responses]
        ok_responses_text = []
        for a, response_text in zip(lis, responses_text, strict=True):
            response_text += f"<source_url>{'https://kmoa.klcg.gov.tw/' + a.attrs.get('href')}</source_url>"
            ok_responses_text.append(response_text)

        return ok_responses_text

    async def fetch_response(self):
        headers = generate_headers(referer="https://kmoa.klcg.gov.tw", need_upgrade_insecure_requests=True)
        cookies = generate_cookies(need_asp_net_session_id=True, other_cookies={"font-size-": "medium"})
        async with HttpxAsyncClient(headers=headers) as client:
            url = "https://kmoa.klcg.gov.tw/News_Photo.aspx?n=7484&sms=12489"
            response = await client.get(url)
            response.raise_for_status()
            responses_data = await self.fetch_sub_response(client, response.text, cookies=cookies)

        return responses_data

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        return parsed


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await KmoaRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
