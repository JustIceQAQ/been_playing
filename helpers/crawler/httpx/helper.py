import httpx2 as httpx

from helpers.crawler.proxy_helper import get_proxy_adapter


class HttpxAsyncClient:
    def __init__(
        self,
        timeout: int | None | httpx.Timeout = None,
        follow_redirects: bool = True,
        use_proxy: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.args = args
        self.kwargs = kwargs
        self.timeout = timeout
        self.use_proxy = use_proxy
        self.follow_redirects = follow_redirects

    async def __aenter__(self) -> httpx.AsyncClient:
        runtime_kwargs = {}
        if self.use_proxy:
            runtime_kwargs["proxies"] = get_proxy_adapter().to_httpx()

        self.client = httpx.AsyncClient(
            *self.args,
            timeout=self.timeout,
            follow_redirects=self.follow_redirects,
            **runtime_kwargs,
            **self.kwargs,
        )
        await self.client.__aenter__()
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.__aexit__(exc_type, exc_val, exc_tb)
