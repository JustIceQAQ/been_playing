import pytest

from helpers.crawler.scrape_do.helper import ScrapeDoAsyncClient


@pytest.mark.asyncio
async def test_get():
    async with ScrapeDoAsyncClient(
        api_key="f196f82e1c6147bd8daa8c1c2893052ddbd94323094"
    ) as client:
        await client.get("https://jam.jutfoundation.org.tw/online-activity")
