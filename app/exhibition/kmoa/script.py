import asyncio
import secrets

import bs4
import httpx

from app.exhibition.kmoa.parse import KmoaParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
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
            fullname="基隆美術館",
            code_name="kmoa",
            external_link="https://kmoa.klcg.gov.tw/News_Photo.aspx?n=7484&sms=12489",
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
        headers = {
            **get_header(),
            "upgrade-insecure-requests": "1",
            "referer": "https://kmoa.klcg.gov.tw",
        }
        cookies = {"ASP.NET_SessionId": secrets.token_hex(12), "font-size-": "medium"}
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
