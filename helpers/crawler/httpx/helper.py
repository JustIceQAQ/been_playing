import httpx2 as httpx

from helpers.crawler.proxy_helper import get_proxy_adapter
from helpers.crawler.ssl_helper import get_ssl_context


class HttpxAsyncClient:
    def __init__(
        self,
        timeout: int | None | httpx.Timeout = None,
        follow_redirects: bool = True,
        use_proxy: bool = False,
        use_certifi_support: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.args = args
        self.kwargs = kwargs
        self.timeout = timeout
        self.use_proxy = use_proxy
        self.follow_redirects = follow_redirects
        self.use_certifi_support = use_certifi_support

    async def __aenter__(self) -> httpx.AsyncClient:
        runtime_kwargs = {
            "timeout": self.timeout,
            "follow_redirects": self.follow_redirects,
        }
        if self.use_certifi_support:
            runtime_kwargs["verify"] = get_ssl_context().to_httpx()
        if self.use_proxy:
            runtime_kwargs["proxy"] = get_proxy_adapter().to_httpx()

        self.client = httpx.AsyncClient(
            *self.args,
            **runtime_kwargs,
            **self.kwargs,
        )

        await self.client.__aenter__()
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.__aexit__(exc_type, exc_val, exc_tb)
