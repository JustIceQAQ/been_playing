import asyncio

import bs4
from app.museums.shungyeart.parse import ShungYeArtParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class ShungYeArtRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = ShungYeArtParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="順益台灣美術館",
            code_name="ShungYeArt",
            external_link="https://www.shungye-art.org/show_now.php",
            branch_coordinates=Coordinate(raw_coordinates="25.046560256806668, 121.51092983908268"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        url = "https://www.shungye-art.org/show_now.php"
        headers = generate_headers(referer=url)
        cookies = generate_cookies(need_phpsessid=True, need_consent=True)

        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(url, cookies=cookies)
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        now = parsed.find("a", {"id": "Now"}).find_all_next(class_="indexnews1")
        notice = parsed.find("a", {"id": "Notice"}).find_all_next(class_="indexnews1")
        now_ex = now + notice
        return now_ex


async def main():
    await ShungYeArtRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
