import httpx


class HttpxAsyncClient:
    def __init__(
        self,
        timeout: int | None | httpx.Timeout = None,
        follow_redirects: bool | None = True,
        *args,
        **kwargs,
    ) -> None:
        self.args = args
        self.kwargs = kwargs
        self.client = httpx.AsyncClient(timeout=timeout, follow_redirects=follow_redirects, *args, **kwargs)

    async def __aenter__(self) -> httpx.AsyncClient:
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
