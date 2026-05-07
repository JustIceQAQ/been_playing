import httpxyz as httpx


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
        self.timeout = timeout
        self.follow_redirects = follow_redirects

    async def __aenter__(self) -> httpx.AsyncClient:
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=self.follow_redirects,
            *self.args,
            **self.kwargs,
        )
        await self.client.__aenter__()
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.__aexit__(exc_type, exc_val, exc_tb)
