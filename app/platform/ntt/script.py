import asyncio

from app.platform.ntt.parse import NTTParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.symbol import VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3, get_this_date_year
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class NTTRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = NTTParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="新北市觀光旅遊網",
            code_name="NTT",
            external_link="https://newtaipei.travel/zh-tw/",
            venue_type=VenueType.PLATFORM,
        )

    async def fetch_response(self):
        year = get_this_date_year()
        headers = generate_headers(
            referer=f"https://newtaipei.travel/zh-tw/calendar/list?year={year}",
            x_requested_with="XMLHttpRequest",
            origin="https://newtaipei.travel",
        )
        data = {"year": year}
        cookies = {}
        async with HttpxAsyncClient(headers=headers) as client:
            html_response = await client.get("https://newtaipei.travel/zh-tw/calendar/list")
            html_response.raise_for_status()
            html_p = BeautifulSoupTranslation().translation_to_object(html_response.text)
            request_verification_token = html_p.select("body > input[name=__RequestVerificationToken]")[0].get("value")
            cookies["__RequestVerificationToken"] = request_verification_token
            headers["content-type"] = "application/json"
            response = await client.post(
                "https://newtaipei.travel/zh-tw/opendata/activities",
                cookies=cookies,
                data=data,
            )
        return response.json()

    async def fetch_parsed(self):
        parsed: dict = await super().fetch_parsed()
        return parsed.get("data")


async def main():
    await NTTRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
