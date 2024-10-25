import asyncio

import pytest

from helpers.crawler.scraper.helper import ScraperAsyncClient


@pytest.mark.asyncio
async def test_get():
    async with ScraperAsyncClient(api_key="c1d7116c9a548d4cc8050f9bf0371e2e") as client:
        await client.get(
            "https://jam.jutfoundation.org.tw/online-activity", sleep_secs=3
        )


@pytest.mark.asyncio
async def test_limit():
    async with ScraperAsyncClient(api_key="94d76e04b5f467df6a0f0e41e69494ad") as client:
        await asyncio.gather(
            *[
                client.get(
                    f"https://jam.jutfoundation.org.tw/online-activity?qq={i}",
                    sleep_secs=3,
                )
                for i in range(10)
            ]
        )
