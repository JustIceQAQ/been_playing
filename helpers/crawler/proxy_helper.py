from functools import lru_cache

from httpx2 import Proxy as Httpx2Proxy
from wreq import Proxy as WreqProxy


class ProxyAdapter:
    def __init__(self, proxy_url: str):
        self.proxy_url = proxy_url

    def to_httpx(self) -> Httpx2Proxy:
        return Httpx2Proxy(url=self.proxy_url)

    def to_niquests(self) -> dict:
        return {"http": self.proxy_url, "https": self.proxy_url}

    def to_wreq(self) -> list[WreqProxy] | None:
        proxies = None if self.proxy_url is None else [WreqProxy.all(self.proxy_url)]

        return proxies


class NoneAdapter:
    def __init__(self, proxy_url: str):
        self.proxy_url = proxy_url

    def to_httpx(self) -> Httpx2Proxy | None:
        return None

    def to_niquests(self) -> dict | None:
        return None

    def to_wreq(self) -> list[WreqProxy] | None:
        return None


@lru_cache
def get_proxy_adapter() -> NoneAdapter:
    from configs.settings import get_settings

    runtime_settings = get_settings()
    return NoneAdapter(runtime_settings.PROXY_POOL)
