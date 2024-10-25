import asyncio
import http

import httpx

from helpers.crawler.scraper.schemas import ScraperResponse


class ScraperAsyncClient:
    def __init__(
        self, api_key: str, timeout: int | None = None, *args, **kwargs
    ) -> None:
        self.args = args
        self.kwargs = kwargs
        self.client = httpx.AsyncClient(timeout=timeout, *args, **kwargs)
        self.api_path = "https://async.scraperapi.com/jobs"
        self.api_key = api_key
        self.job_status_url = None
        self.job_status = False

    async def get(
        self, url: str, render=True, headers=None, sleep_secs=20, tries_flag=5
    ) -> ScraperResponse:
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
            return ScraperResponse(status_code=response.status_code)

        while response.status_code == http.HTTPStatus.TOO_MANY_REQUESTS:
            await asyncio.sleep(sleep_secs)
            response = await self.client.post(self.api_path, json=payload)

        this_response = ScraperResponse.model_validate(
            {**response.json(), "status_code": response.status_code}
        )
        runtime_flag = 0
        while this_response.is_running:
            if runtime_flag == tries_flag:
                break
            await asyncio.sleep(sleep_secs)
            response = await self.client.get(this_response.status_url)
            this_response = ScraperResponse.model_validate(
                {**response.json(), "status_code": response.status_code}
            )
            runtime_flag += 1
        return this_response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
