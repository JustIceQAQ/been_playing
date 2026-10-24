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
        disable_ipv6: bool = True,
        *args,
        **kwargs,
    ) -> None:
        self.args = args
        self.kwargs = kwargs
        self.timeout = timeout
        self.use_proxy = use_proxy
        self.follow_redirects = follow_redirects
        self.use_certifi_support = use_certifi_support
        self.disable_ipv6 = disable_ipv6

    async def __aenter__(self) -> httpx.AsyncClient:
        kwargs = dict(self.kwargs)
        verify = kwargs.pop("verify", None)

        if verify is None and self.use_certifi_support:
            verify = get_ssl_context().to_httpx()

        runtime_kwargs = {
            "timeout": self.timeout,
            "follow_redirects": self.follow_redirects,
        }
        if verify is not None:
            runtime_kwargs["verify"] = verify
        if self.use_proxy:
            runtime_kwargs["proxy"] = get_proxy_adapter().to_httpx()
        if self.disable_ipv6:
            transport_kwargs = {"local_address": "0.0.0.0"}
            if verify is not None:
                transport_kwargs["verify"] = verify
            runtime_kwargs["transport"] = httpx.AsyncHTTPTransport(**transport_kwargs)
        self.client = httpx.AsyncClient(*self.args, **runtime_kwargs, **kwargs)
        await self.client.__aenter__()
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.__aexit__(exc_type, exc_val, exc_tb)
