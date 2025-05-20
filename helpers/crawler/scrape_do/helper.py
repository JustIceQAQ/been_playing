import asyncio
from urllib.parse import urlencode

import httpx

from .schemas import Response, ScrapeDoResponse


class ScrapeDoAsyncClient:
    def __init__(
        self, api_key: str, timeout: int | None = None, *args, **kwargs
    ) -> None:
        self.args = args
        self.kwargs = kwargs
        self.client = httpx.AsyncClient(timeout=timeout, *args, **kwargs)
        self.api_path = "http://api.scrape.do"
        self.api_key = api_key

    async def get(
        self,
        url: str,
        headers=None,
        render=True,
        return_json: bool | None = False,
        sleep_secs=20,
        tries_flag=5,
    ):
        query_parameters = urlencode(
            {
                "token": self.api_key,
                "url": url,
                "render": render,
                "returnJSON": return_json,
            }
        )
        response = await self.client.get(
            f"{self.api_path}?{query_parameters}", headers=headers
        )
        if response.is_client_error or response.is_server_error:
            return ScrapeDoResponse(
                status_code=response.status_code, is_success=response.is_success
            )
        error_flag = 0
        while response.is_redirect:
            error_flag += 1
            if error_flag == tries_flag:
                break
            await asyncio.sleep(sleep_secs)
            response = await self.client.get(
                f"{self.api_path}?{query_parameters}", headers=headers
            )

        if error_flag == tries_flag:
            return ScrapeDoResponse(
                status_code=response.status_code, is_success=response.is_success
            )

        body = response.json() if return_json else response.text
        return ScrapeDoResponse(
            status_code=response.status_code,
            response=Response(body=body),
            is_success=response.is_success,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
