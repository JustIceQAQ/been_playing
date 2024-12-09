import asyncio
import secrets

import bs4

from app.exhibition.museumpost.parse import MuseumPostParse
from helpers.cache.none.helper import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class MuseumPostRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = MuseumPostParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="郵政博物館",
            code_name="MuseumPost",
            external_link="https://museum.post.gov.tw/post/Postal_Museum/museum/index.jsp?ID=131&topage=1",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "Host": "museum.post.gov.tw",
            "Cookie": f"JSESSIONID={secrets.token_hex(16).upper()}",
            "Connection": "keep-alive",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            target_url = "https://museum.post.gov.tw/post/Postal_Museum/museum/index.jsp?ID=131&topage={to_page}"
            responses = []
            page = 1
            response = await client.get(target_url.format(to_page=page))
            while (
                self.translation()
                .translation_to_object(response.text)
                .select("ul.part_list > li")
            ):
                responses.append(response.text)
                page += 1
                response = await client.get(target_url.format(to_page=page))

            return responses

    async def fetch_parsed(self):
        parsers: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        items = []
        for parsed in parsers:
            items.extend(parsed.select("ul.part_list > li"))
        return items


async def main():
    await MuseumPostRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
