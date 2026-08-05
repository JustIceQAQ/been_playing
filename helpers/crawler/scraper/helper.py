import asyncio
import http
import random

import httpx

from helpers.crawler.scraper.schemas import ScraperJobsResponse

SCRAPER_ASYNC_CLIENT = set()
AVAILABLE_POOL = set()


class ScraperAsyncClient:
    def __init__(self, api_key: str, timeout: int | None = None, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.client = httpx.AsyncClient(*args, timeout=timeout, **kwargs)
        self.api_path = "https://async.scraperapi.com/jobs"
        self.api_key = api_key
        self.job_status_url = None
        self.job_status = False
        self.available_info = None

    async def get(
        self,
        url: str,
        render=True,
        headers=None,
        sleep_secs=20,
        tries_flag=5,
        *args,
        **kwargs,
    ) -> ScraperJobsResponse:
        payload = {
            "apiKey": self.api_key,
            "url": url,
            "render": render,
            "method": "GET",
        }
        if headers is not None:
            payload["headers"] = headers
        response = await self.client.post(self.api_path, json=payload)
        if response.status_code in {
            http.HTTPStatus.BAD_REQUEST,
            http.HTTPStatus.NOT_FOUND,
            http.HTTPStatus.GONE,
            http.HTTPStatus.INTERNAL_SERVER_ERROR,
            http.HTTPStatus.FORBIDDEN,
        }:
            return ScraperJobsResponse(status_code=response.status_code)

        while response.status_code == http.HTTPStatus.TOO_MANY_REQUESTS:
            await asyncio.sleep(sleep_secs)
            response = await self.client.post(self.api_path, json=payload)
        response.raise_for_status()
        this_response = ScraperJobsResponse.model_validate({**response.json(), "status_code": response.status_code})
        runtime_flag = 0
        while this_response.is_running:
            if runtime_flag == tries_flag:
                break
            await asyncio.sleep(sleep_secs)
            response = await self.client.get(this_response.status_url)
            this_response = ScraperJobsResponse.model_validate({**response.json(), "status_code": response.status_code})
            runtime_flag += 1
        return this_response

    async def get_available_info(self):
        url = "https://api.scraperapi.com/account"
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(url, params={"api_key": self.api_key})
            if response.is_success:
                self.available_info = response.json()
                SCRAPER_ASYNC_CLIENT.add(self)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()


def get_a_available_scraper_async_client() -> ScraperAsyncClient:
    return random.choice(tuple(SCRAPER_ASYNC_CLIENT))


async def available_scraper_async_client(keys: list[str] | None):
    if keys is None:
        raise ValueError("Scraper keys is not provided")
    await asyncio.gather(*[ScraperAsyncClient(api_key=key).get_available_info() for key in keys])
    for client in SCRAPER_ASYNC_CLIENT:
        available_info = client.available_info
        if available_info["requestLimit"] != 0 and available_info["requestLimit"] < available_info["requestCount"]:
            SCRAPER_ASYNC_CLIENT.add(client)
