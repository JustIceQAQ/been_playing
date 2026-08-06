import asyncio

from app.museums.bopiliao.parse import BoPiLiaoParse
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class BoPiLiaoRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = BoPiLiaoParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.wanhua_63000070,
            fullname="剝皮寮歷史街區",
            code_name="BoPiLiao",
            external_link="https://www.bopiliao.taipei/Event_News",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.03698373119932, 121.50212186318004"),
                raw_coordinates="25.03698373119932, 121.50212186318004",
            ),
            venue_type=VenueType.MEMORIAL,
        )

    async def _fetch_url(self, client, url: str, params: dict):
        return await client.get(url, params=params)

    async def fetch_response(self):
        headers = generate_headers(host="www.bopiliao.taipei")
        params = {
            "ajax": 1,
            "search_day_start": "",
            "search_day_end": "",
            "pageSize": 10,
            "pageNumber": 1,
        }
        urls = (
            "https://www.bopiliao.taipei/Event_News/new",
            "https://www.bopiliao.taipei/Event_News/now",
        )

        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [self._fetch_url(client, url, params) for url in urls]
            tasks_response = await asyncio.gather(*tasks)
        return tasks_response

    async def fetch_parsed(self):
        items = []
        parsed = await super().fetch_parsed()
        for item in parsed:
            items.extend(item.json()["items"])
        return items


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await BoPiLiaoRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
