import pytest

from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header


@pytest.mark.asyncio
async def test_get():
    async with HttpxAsyncClient() as client:
        response = await client.get(
            "https://www.klook.com/v1/enteventapisrv/public/content/query_v3"
            "?k_lang=zh_TW"
            "&k_currency=TWD"
            "&area=city_19"
            "&page_size=50"
            "&page_num=1"
            "&filters=convention_exhibition"
            "&sort=latest"
            "&date=next_30_days"
            "&start_date="
            "&end_date="
            "&keywords=",
            headers={
                **get_header(),
                "accept": "text/html,"
                "application/xhtml+xml,"
                "application/xml;q=0.9,"
                "image/avif,image/webp,"
                "image/apng,*/*;q=0.8,"
                "application/signed-exchange;v=b3;q=0.7",
                "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            },
        )
        response_json = response.json()
        print(response_json)
