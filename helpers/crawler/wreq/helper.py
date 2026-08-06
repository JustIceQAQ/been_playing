import wreq

from helpers.crawler.proxy_helper import get_proxy_adapter


class WReqAsyncClient:
    def __init__(self, *args, use_proxies: bool = False, **kwargs) -> None:
        runtime_kwargs = {}
        if use_proxies:
            runtime_kwargs["proxies"] = get_proxy_adapter().to_wreq()
        self.client = wreq.Client(
            *args,
            emulation=wreq.Emulation(profile=wreq.Profile.Firefox149),
            redirect=wreq.redirect.Policy.limited(10),
            **runtime_kwargs,
            **kwargs,
        )

    async def __aenter__(self) -> wreq.Client:
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
