import asyncio

from app.platform.iculture.parse import ICultureParse
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.symbol import VenueType
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class ICultureRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = ICultureParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="iCulture 藝文資源資訊平台",
            code_name="iCulture",
            external_link="https://cloud.culture.tw/",
            venue_type=VenueType.PLATFORM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            referer="https://cloud.culture.tw/frontsite/inquiry/eventInquiryAction.do?method=showEventList",
            host="cloud.culture.tw",
        )
        params = {
            "page": 0,
            "size": 100,
            "sort": "id",
            "category": "6",
            "onSale": 0
        }
        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [
                client.get(
                    "https://cloud.culture.tw/data/api/frontsite/inquiry/event",
                    params=params | {"cityName": city_name},
                )
                for city_name in ["臺北市", "新北市"]
            ]
            responses = await asyncio.gather(*tasks)
        return [response.json() for response in responses]

    async def fetch_parsed(self):
        parsed: list[dict] = await super().fetch_parsed()
        datas = []
        for data in parsed:
            datas.extend(data.get("rows"))
        return datas


async def main():
    await ICultureRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
