import asyncio

import bs4
import httpx

from app.exhibition.kmoa.parse import KmoaParse
from helpers.headers_helper import get_headers, get_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class KmoaRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KmoaParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.keelung_city,
            fullname="基隆美術館",
            code_name="kmoa",
            external_link="https://kmoa.klcg.gov.tw/News_Photo.aspx?n=7484&sms=12489",
            branch_coordinates=Coordinate(raw_coordinates="25.131248388298207, 121.74399937483508"),
        )

    async def fetch_sub_response(
            self, client: httpx.AsyncClient, context: str
    ) -> list[str]:
        p = BeautifulSoupTranslation().translation_to_object(context)
        div = p.find("div", {"class": "group-list page-block PhotoList"})
        if div is None:
            return []
        lis = div.find_all("a")
        tasks = [client.get("https://kmoa.klcg.gov.tw/" + a["href"]) for a in lis]
        responses = await asyncio.gather(*tasks)
        responses_text = [response.text for response in responses]
        ok_responses_text = []
        for a, response_text in zip(lis, responses_text):
            response_text += (
                f"<source_url>{"https://kmoa.klcg.gov.tw/" + a["href"]}</source_url>"
            )
            ok_responses_text.append(response_text)

        return ok_responses_text

    async def fetch_response(self):
        headers = get_headers(
                referer="https://kmoa.klcg.gov.tw",
                need_upgrade_insecure_requests=True
            )
        cookies = {**get_cookies(need_asp_net_session_id=True), "font-size-": "medium"}
        async with HttpxAsyncClient(headers=headers, cookies=cookies) as client:
            url = "https://kmoa.klcg.gov.tw/News_Photo.aspx?n=7484&sms=12489"
            response = await client.get(url)
            responses_data = await self.fetch_sub_response(client, response.text)

        return responses_data

    async def fetch_parsed(self):
        parsed: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        return parsed


async def main():
    await KmoaRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
